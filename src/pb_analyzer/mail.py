import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from loguru import logger


def prepare_message(sender, recipient, subject, content) -> MIMEMultipart:
    message = MIMEMultipart()
    message['From'] = sender
    message['To'] = recipient
    message['Subject'] = subject
    message.attach(MIMEText(content, 'html'))
    return message


def send_mail(server, port, user, password, message: MIMEMultipart):
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(server, port, context=context) as server:
        server.login(user, password)
        server.sendmail(message['From'], message['To'], message.as_string())
    logger.info('Sent e-mail')
