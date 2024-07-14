import smtplib
from email.mime.text import MIMEText

from config import EMAIL_HOST, EMAIL_PASSWORD, EMAIL_USER


def send_email(email_body):
    msg = MIMEText(email_body)
    msg["Subject"] = "Relatório Semanal de Feedbacks"
    msg["From"] = EMAIL_USER
    msg["To"] = EMAIL_USER

    with smtplib.SMTP(EMAIL_HOST, 587) as server:
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASSWORD)
        server.send_message(msg)
