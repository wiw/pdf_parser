import argparse
import copy
import io
import os
import re

import pandas as pd

from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage

import tabula

config = {
    "doctor_regex": ".* (?P<sname>[А-Яа-я].*) \
(?P<flname>[А-Я]\\..?[А-Я]\\.).*",
    "excel_sheet_name": 'Информация о записях и приемах',
    "first_line_range": 200,
    "default_filename": "output.xlsx",
}


def parse_arguments():
    p = argparse.ArgumentParser(
        description="Convert some pdf files of \
medical department to tabulated view")
    p.add_argument(
        "source_dir", help="path to folder with your \
pdf files and single xls file", type=str)
    p.add_argument("-o", "--output", help="path to output folder")
    args = p.parse_args()
    return args


def from_pdf_get_first_line(pdf_path, config):
    def extract_text_by_page(pdf_path):
        with open(pdf_path, 'rb') as fh:
            for page in PDFPage.get_pages(fh,
                                          caching=True,
                                          check_extractable=True):
                resource_manager = PDFResourceManager()
                fake_file_handle = io.StringIO()
                converter = TextConverter(resource_manager, fake_file_handle)
                page_interpreter = PDFPageInterpreter(
                    resource_manager, converter)
                page_interpreter.process_page(page)
                text = fake_file_handle.getvalue()
                yield text
                converter.close()
                fake_file_handle.close()

    def extract_doctors_name(string, doctor_regex):
        regexp = re.compile(doctor_regex)
        match = regexp.match(string)
        if match is not None:
            doctor_name = match.groupdict()
            doctor_name['flname'] = doctor_name['flname'].replace(" ", "")
            return doctor_name
        else:
            return None
    filename = os.path.splitext(os.path.basename(pdf_path))[0]
    data = {'filename': filename,
            "header": {},
            "body": {},
            }
    counter = 1
    for page in extract_text_by_page(pdf_path):
        string = page[:config['first_line_range']]
        data['header'].setdefault(
            counter, extract_doctors_name(string, config['doctor_regex']))
        counter += 1
    return data


def pdf_to_dataframe(pdf_path, page_number):
    temp = tabula.read_pdf(pdf_path, options='--pages {}'.format(page_number))
    return temp


def select_files(source_path):
    sources, files = {}, []
    try:
        if os.path.isdir(source_path):
            for f in os.listdir(source_path):
                if os.path.isfile(os.path.join(source_path, f)):
                    files.append(os.path.join(source_path, f))
            sources.setdefault('pdf', [p for p in files if re.match(
                ".*pdf$", os.path.basename(p)) is not None])
            sources.setdefault('xlsx', [x for x in files if re.match(
                ".*xlsx$", os.path.basename(x)) is not None])
            return sources
        else:
            print("I did not find the files you need")
            raise SystemExit
    except Exception as e:
        raise e


def parse_pdf(config):
    data, counter = {}, 1
    for pfile in config['pdf']:
        # !NB TASK1: add progress bar per pdf file and per page
        parsed_pdf = from_pdf_get_first_line(pfile, config)
        for page_number in parsed_pdf['header'].keys():
            parsed_pdf['body'].setdefault(
                page_number, pdf_to_dataframe(pfile, page_number))
        data.setdefault(counter, parsed_pdf)
        counter += 1
    return data


def beautiful_pdf(data):
    output = copy.deepcopy(data)
    for file_pos, pdf in data.items():
        range_values = pdf['body'].keys()
        for page in range_values:
            page_df = pdf['body'][page]
            tmp_df = page_df.iloc[2:, [0, 1, 3]].dropna(how='all')
            tmp_df.columns = ['date', 'district', 'phone']
            output[file_pos]['body'][page] = tmp_df
    return output


def format_pdf(data):
    output = {}

    def get_date(col):
        timestamp = []
        date_tmp = col.dropna().reset_index().date
        for idx in date_tmp.keys():
            if idx == 0 or idx % 2 == 0:
                date_string = "{} {}".format(date_tmp[idx], date_tmp[idx + 1])
                timestamp.append(pd.to_datetime(date_string))
        return pd.Series(timestamp)

    def get_district(col):
        district_strings = col.str.cat(sep=" ").split(") К")
        regex = re.compile(".*?\\((?P<district>.*No[0-9]{1,2}).*")
        district_strings_filtered = [
            regex.sub('\\g<district>', item) for item in district_strings]
        return pd.Series(district_strings_filtered)

    def get_phone(col):
        phone_strings = col.str.cat(sep=" ", na_rep="+7 000 000-00-00") + " "
        re_phone_split = re.compile('(?:(?:\\+7 [0-9]{3} \
[0-9]{3}-[0-9]{2}-[0-9]{2} )+)+')
        phone_strings = re_phone_split.findall(phone_strings)
        phone_strings = [x[:-1] for x in phone_strings]
        re_phone_sep = re.compile('(\\+7 [0-9]{3} [-0-9]*).*')
        phone_strings = [re_phone_sep.sub(
            '\\1', x) for x in phone_strings]
        return pd.Series(phone_strings)
    for item, pdf in data.items():
        concat_list = []
        for number, df in pdf['body'].items():
            date = get_date(df.date)
            district = get_district(df.district)
            phone = get_phone(df.phone)
            list_of_series = [date, district, phone]
            cols = ['date', 'district', 'phone']
            tmp_df = pd.concat(list_of_series, axis=1, ignore_index=True)
            tmp_df.columns = cols
            tmp_df['doctor'] = " ".join([pdf['header'][number]['sname'],
                                         pdf['header'][number]['flname']])
            concat_list.append(tmp_df)
        pre_output = pd.concat(concat_list, ignore_index=True)
        pre_output = pre_output[pre_output.phone != '+7 000 000-00-00']
        output.setdefault(pdf['filename'],
                          pd.concat(concat_list, ignore_index=True))
    return output


def parse_excel(config):
    def format_doctor_name(col):
        tmp = col.tolist()
        re_doctor = re.compile('(^[-а-яА-Я]*) ([А-Я]).*([А-Я]).*')
        tmp = [re_doctor.sub('\\1 \\2.\\3.', x) for x in tmp]
        return pd.Series(tmp, name='doctor')

    def format_date(df):
        sample_df = df.loc[:, ['date', 'ptime', 'ftime']]
        sample_df.date = sample_df.date.dt.strftime('%Y-%m-%d')
        proposed = pd.to_datetime(
            sample_df.date.map(str) + ' ' + sample_df.ptime)
        fact = pd.to_datetime(sample_df.date.map(str) + ' ' + sample_df.ftime)
        output = pd.concat([proposed, fact], axis=1, ignore_index=True)
        output.columns = ['ptime', 'ftime']
        return output

    def main_format(unformatted):
        formatted = copy.deepcopy(unformatted)
        formatted.update(format_doctor_name(unformatted.doctor))
        update_v = [formatted.loc[:, ['doctor', 'duration']],
                    format_date(unformatted)]
        formatted = pd.concat(update_v, axis=1, ignore_index=True)
        formatted.columns = ['doctor', 'duration', 'date', 'ftime']
        formatted.duration = pd.to_numeric(formatted.duration,
                                           downcast='signed',
                                           errors='coerce').dropna()
        formatted = formatted[formatted.duration.notnull()]
        return formatted
    if len(config['xlsx']) == 1:
        excel_df = pd.read_excel(
            config['xlsx'][0], sheet_name=config['excel_sheet_name'])
        excel_df = excel_df.iloc[3:, [0, 3, 4, 6, 7]]
        excel_df.columns = ['doctor', 'date', 'ptime', 'ftime', 'duration']
        excel_df = main_format(excel_df)
        return excel_df
    else:
        print("Need only one Excel File. Exit...")
        raise SystemExit


def filter_visits(input_dfs, filter_df):
    output = {}
    for filename, df in input_dfs.items():
        tmp = pd.merge(df, filter_df, how='inner', on=['doctor', 'date'])
        tmp = tmp[['doctor', 'date', 'district', 'phone']]
        output.setdefault(filename, tmp)
    return output


def write_data(data, args, config):
    default_path = os.path.dirname(config['xlsx'][0])
    if args.output is not None and os.path.exists(args.output):
        default_path = args.output
    path_name = os.path.join(default_path, config['default_filename'])
    with pd.ExcelWriter(path_name) as writer:
        for district_name, df in data.items():
            df.to_excel(writer, sheet_name=district_name)


def load_pdf(config):
    data = parse_pdf(config)
    parsed_data = beautiful_pdf(data)
    formatted_data = format_pdf(parsed_data)
    return formatted_data


def view_cli(args, config):
    loaded_pdf = load_pdf(config)
    excel_df = parse_excel(config)
    joined_df = filter_visits(loaded_pdf, excel_df)
    return joined_df


def main(args, config):
    config.update(select_files(args.source_dir))
    result = view_cli(args, config)
    write_data(result, args, config)


if __name__ == '__main__':
    args = parse_arguments()
    main(args, config)

# args = p.parse_args(['--output', '/home/aivankin/',\
# '/home/aivankin/SOURCE/'])
