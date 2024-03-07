import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from pydantic import EmailStr

from config import SMTP_REPRESENTER, SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASS


def send_registration_email(user_email: EmailStr):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Welcome to our Chat!"
    msg["From"] = SMTP_REPRESENTER
    msg["To"] = user_email
    html = """
    <html>
  <head></head>
  <body>
    <h1>You have successfully registered on our website! Hope you <b>like</b> it!</h1>
    
  </body>
</html>
        """
    html_part = MIMEText(html, "html")
    msg.attach(html_part)
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as smtp:
        smtp.login(SMTP_USER, SMTP_PASS)
        smtp.send_message(msg)
