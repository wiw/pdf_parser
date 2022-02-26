import logging
import smtplib, ssl

from email import encoders
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase

from typing import Optional
from pydantic import FilePath

from classic.components import component

from questionnaire.application import interfaces, dataclasses
from .settings import EmailSettings


@component
class FileMailSender(interfaces.IMailSender):
    logger: Optional[logging.Logger] = None

    def __attrs_post_init__(self):
        if self.logger is None:
            self.logger = logging.getLogger(self.__class__.__name__)

    def send(self, mail: dataclasses.Report):
        self.logger.info(
            'SendTo: {%s}\n'
            'Title: {%s}\n'
            'Body: {%s}\n',
            mail.email.full_name,
            mail.email.title,
            mail.email.body,
        )
        with self._connect() as server:
            server.login(
                user=EmailSettings.EMAIL_USER,
                password=EmailSettings.EMAIL_PASS
            )
            server.sendmail(
                mail.email.email_address,
                EmailSettings.EMAIL_ADDRESS,
                self._create_message(mail)
            )

    def _create_message(self, mail: dataclasses.Report) -> str:
        message = MIMEMultipart()
        message['From'] = mail.email.email_address
        message['To'] = EmailSettings.EMAIL_ADDRESS
        message['Subject'] = mail.email.title
        message['bcc'] = EmailSettings.EMAIL_ADDRESS

        message.attach(MIMEText(mail.email.body, 'plain'))

        message.attach(self._add_attachment(mail.file_path))
        return message.as_string()

    @staticmethod
    def _add_attachment(filename: FilePath) -> MIMEBase:
        with open(filename, 'rb') as attachment:
            attach = MIMEBase('application', 'octet-stream')
            attach.set_payload(attachment.read())

        encoders.encode_base64(attach)

        attach.add_header(
            'Content-Disposition',
            f'attachment; filename= {filename}',
        )

        return attach

    @staticmethod
    def _connect() -> smtplib.SMTP_SSL:
        context = ssl.create_default_context()
        return smtplib.SMTP_SSL(
            EmailSettings.EMAIL_SERVER,
            EmailSettings.EMAIL_SMTP_PORT,
            context=context
        )
