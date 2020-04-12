"""
Описание.

Программа для парсинга pdf файлов и обработки пересечений данных с файлом
Excel.

Обязательные аргументы:

    путь до папки с исходными файлами pdf&xls(x)

Необязательные аргументы

    -o путь до папки с результатом
    -sn опциональное имя листа в файле Excel, если оно отличается о такового
    в переменной config["excel_sheet_name"]
"""

import argparse
import copy
import io
import os
import re
import operator as op

import pandas as pd

from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage

from progressbar import Bar
from progressbar import ProgressBar as Pg

import tabula

# from pprint import pprint as view


"""
Словарь с необходимой конфишурацией для запуска программы.

    doctor_regex: регулярное выражение для поиска ФИО врача в заголовке
    страницы

    excel_sheet_name: наименование листа в калибровочном файле Excel

    first_line_range: количество символов используемых в качестве заголовка
    листа

    default_filename: имя файла с результатом по умолчанию
"""
config = {
    "doctor_regex": "20[0-9]{2}(?P<full_match>[Ф|ДГП][0-9А-Яа-я\\. \
]*\\(к.[0-9\\-А-Я]*\\))",
    "excel_sheet_name": 'Информация о записях и приемах',
    "first_line_range": 200,
    "default_filename": "output.xlsx",
}


def parse_arguments():
    """
    Обработчик аргументов.
    """
    p = argparse.ArgumentParser(
        description="Программа конвертации pdf файлов \
и вывода табличных отформатированных данных")
    p.add_argument(
        "source_dir", help="Путь до папки с исходными файлами", type=str)
    p.add_argument("-o", "--output", help="Необязательно. \
Путь до папки с обработанным результатом", type=str)
    p.add_argument("-sn", "--sheet_name", help="Наименование листа с \
калибровочными данными в xls/xlsx документе", type=str)
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
        match = regexp.search(string)
        doctor_name = None
        if match is not None:
            raw_full_name = match.groupdict()
            doctor_name = raw_full_name["full_match"]

        return doctor_name

    filename = os.path.splitext(os.path.basename(pdf_path))[0]
    data = {'filename': filename,
            "header": {},
            "body": {},
            "just_in_case": {}
            }
    counter = 1

    for page in extract_text_by_page(pdf_path):
        string = page[:config['first_line_range']]
        data['header'].setdefault(
            counter, extract_doctors_name(string, config['doctor_regex']))
        data["just_in_case"].setdefault(counter, page)
        counter += 1

    return data


def pdf_to_dataframe(pdf_path, page_number):
    temp = tabula.read_pdf(pdf_path,
                           pages=page_number,
                           pandas_options={"header": None})
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
            print("В указанной папке нет файлов для обработки. \
Проверьте еще раз. Выход...")
            raise SystemExit
    except Exception as e:
        raise e


def parse_pdf(config):
    data, counter = {}, 1

    for pfile in config['pdf']:
        print("Загружаю файл {} ...".format(os.path.basename(pfile)))
        try:
            parsed_pdf = from_pdf_get_first_line(pfile, config)
            page_numbers = len(parsed_pdf['header'])
            bar = Pg(maxval=page_numbers,
                     widgets=[Bar(left='<', marker='.', right='>')]).start()
            t = 0
            for page_number in parsed_pdf['header'].keys():
                bar.update(t)
                t += 1
                page_parsed = pdf_to_dataframe(pfile, page_number)
                if page_parsed is None:
                    continue
                parsed_pdf['body'].setdefault(page_number, page_parsed)
            data.setdefault(counter, parsed_pdf)
            counter += 1
            bar.finish()
        except Exception as e:
            print("Не могу загрузить \
файл {}, пропускаю ...\n\
Exception: {}".format(os.path.basename(pfile), type(e).__name__))
            next
    return data


def beautiful_pdf(data):
    output = copy.deepcopy(data)
    broken_pages = {}

    for file_pos, pdf in data.items():
        range_values = pdf['body'].keys()
        for page in range_values:

            page_df, start_row = pdf['body'][page], 0
            if page_df.iloc[0, 0] == 'Дата и':
                start_row = 3
            if page_df.iloc[:, 3].isnull().all():
                broken_pages.setdefault(file_pos, [])
                broken_pages[file_pos].append(page)
            vector_col = [0, 1, 3]
            tmp_df = page_df.iloc[start_row:, vector_col].dropna(how='all')
            tmp_df.columns = ['date', 'district', 'phone']
            output[file_pos]['body'][page] = tmp_df

    return output, broken_pages


def format_pdf(data, broken_data):
    output = {}

    def broken_exists(broken_data, item, number):
        result = []
        if op.eq(len(broken_data), 0):
            return False
        result.append(op.ne(len(broken_data[item]), 0))
        result.append(op.contains(broken_data[item], number))
        return all(result)

    def get_date(col):
        timestamp = []
        date_tmp = col.dropna().reset_index().date
        for idx in date_tmp.keys():
            if idx == 0 or idx % 2 == 0:
                date_string = "{} {}".format(date_tmp[idx], date_tmp[idx + 1])
                timestamp.append(pd.to_datetime(date_string,
                                                format='%d.%m.%Y %H:%M'))
        return pd.Series(timestamp)

    def get_district(col):
        district_strings = col.str.cat(sep=" ").split(") К")
        regex = re.compile(".*?\\((?P<district>.*No[0-9]{1,2}).*")
        district_strings_filtered = [
            regex.sub('\\g<district>', item) for item in district_strings]
        return pd.Series(district_strings_filtered)

    def get_phone(col):
        phone_strings = col
        if isinstance(col, pd.core.series.Series):
            phone_strings = col.str.cat(sep="", na_rep="+7 000 000-00-00")
        re_phone_split = re.compile('(?:(?:\\+7 [0-9]{3} \
[0-9]{3}-[0-9]{2}-[0-9]{2})+)+')
        phone_strings = re_phone_split.findall(phone_strings)
        re_phone_sep = re.compile('(\\+7 [0-9]{3} [-0-9]*).*')
        phone_strings = [re_phone_sep.sub('\\1', x) for x in phone_strings]
        return pd.Series(phone_strings)

    for item, pdf in data.items():
        concat_list = []
        for number, df in pdf['body'].items():
            date = get_date(df.date)
            district = get_district(df.district)
            raw_phone = df.phone
            if broken_exists(broken_data, item, number):
                raw_phone = op.getitem(pdf['just_in_case'], number)
            phone = get_phone(raw_phone)
            list_of_series = [date, district, phone]
            cols = ['date', 'district', 'phone']
            tmp_df = pd.concat(list_of_series, axis=1, ignore_index=True)
            tmp_df.columns = cols
            tmp_df['doctor'] = pdf['header'][number]
            concat_list.append(tmp_df)
        pre_output = pd.concat(concat_list, ignore_index=True)
        pre_output = pre_output[pre_output.phone != '+7 000 000-00-00']
        output.setdefault(pdf['filename'], pre_output)
    return output


def parse_excel(config, args):

    def format_doctor_name(col):
        tmp = col.tolist()
        re_doctor = re.compile('(^[-а-яА-Я]*) ([А-Я]).*([А-Я]).*')
        tmp = [re_doctor.sub('\\1 \\2.\\3.', x) for x in tmp]
        return pd.Series(tmp, name='doctor')

    def format_date(df):
        sample_df = df.loc[:, ['date', 'ptime', 'ftime']]
        sample_df.date = sample_df.date.dt.strftime('%Y-%m-%d')
        proposed = pd.to_datetime(sample_df.date.map(str) +
                                  ' ' +
                                  sample_df.ptime)
        fact = pd.to_datetime(sample_df.date.map(str) +
                              ' ' +
                              sample_df.ftime)
        output = pd.concat([proposed, fact], axis=1, ignore_index=True)
        output.columns = ['ptime', 'ftime']
        return output

    def main_format(unformatted):
        formatted = copy.deepcopy(unformatted)
        update_v = [formatted.loc[:, ['doctor', 'duration']],
                    format_date(unformatted)]
        formatted = pd.concat(update_v, axis=1, ignore_index=True)
        formatted.columns = ['doctor', 'duration', 'date', 'ftime']
        formatted.duration = pd.to_numeric(formatted.duration,
                                           downcast='signed',
                                           errors='coerce').dropna()
        formatted = formatted[formatted.duration.notnull()]
        return formatted

    def get_sheet_name(config, args):
        if args.sheet_name is not None:
            return args.sheet_name
        return config['excel_sheet_name']

    if len(config['xlsx']) == 1:
        excel_df = pd.read_excel(
            config['xlsx'][0], sheet_name=get_sheet_name(config, args))
        excel_df = excel_df.iloc[3:, [2, 4, 5, 7, 8]]
        excel_df.columns = ['doctor', 'date', 'ptime', 'ftime', 'duration']
        excel_df = main_format(excel_df)
        return excel_df
    else:
        print("Нужен только один файл Excel. Выход...")
        raise SystemExit


def filter_visits(input_dfs, filter_df):
    output = {}
    for filename, df in input_dfs.items():
        tmp = pd.merge(df, filter_df, how='inner', on=['doctor', 'date'])
        tmp = tmp[['doctor', 'date', 'date', 'phone']]
        output.setdefault(filename, tmp)
    return output


def write_data(data, args, config):
    default_path = os.path.join(os.path.dirname(config['xlsx'][0]), "output")

    if args.output is not None and os.path.exists(args.output):
        default_path = args.output

    if not os.path.exists(default_path):
        os.makedirs(default_path)

    path_name = os.path.join(default_path, config['default_filename'])
    pname_robot = os.path.join(default_path, 'call_robot.csv')
    print("Записываю обработанные таблицы в файл {}".format(path_name))

    with pd.ExcelWriter(path_name) as writer:
        merged_data = pd.DataFrame()
        for district_name, df in data.items():
            if df.empty:
                print("    Файл '{}' не прошел калибровку.\n\
        Пропускаю...".format(district_name))
                next
            df.to_excel(writer, sheet_name=district_name)
            merged_data = pd.concat([merged_data, df.iloc[:, [2, 3]]])
            merged_data.to_csv(pname_robot, header=False)
    print("Готово\nВыход.")


def load_pdf(config):
    data = parse_pdf(config)
    print("Распознаю полученные файлы...")
    parsed_data, broken_data = beautiful_pdf(data)
    formatted_data = format_pdf(parsed_data, broken_data)
    return formatted_data


def view_cli(args, config):
    loaded_pdf = load_pdf(config)
    print("Загружаю и распознаю калибровочный xls/xlsx файл...")
    excel_df = parse_excel(config, args)
    print("Фильтрую данные...")
    joined_df = filter_visits(loaded_pdf, excel_df)
    return joined_df


def main(args, config):
    config.update(select_files(args.source_dir))
    result = view_cli(args, config)
    write_data(result, args, config)


if __name__ == '__main__':
    args = parse_arguments()
    main(args, config)
