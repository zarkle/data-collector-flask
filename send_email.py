from email.mime.text import MIMEText
import smtplib


def send_email(email, height):
    """Function to send average height to entered email."""
    from_email = 'django.ab.123@gmail.com'
    from_password = 'bev12345'
    to_email = email

    subject = 'Height data'
    message = f'Hello, your height is <strong>{height}</strong>.'

    msg = MIMEText(message, 'html')
    msg['Subject'] = subject
    msg['To'] = to_email
    msg['From'] = from_email

    gmail = smtplib.SMTP('smtp.gmail.com', 587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(from_email, from_password)
    gmail.send_message(msg)
