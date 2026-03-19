import smtplib
from email.message import EmailMessage
import os
from fastapi import HTTPException

def send_email(response_llm: str, smtp_server: str, port: int, mail_receiver: str):
    mail_user = "rvn@gmail.com"
    mail_user_pwd = os.getenv("app_pwd_user")
    content_msg = response_llm

    email = EmailMessage()

    email["From"] = mail_user
    email["To"] = mail_receiver
    email["Subject"] = "Issue(s) report" 

    email.set_content(content_msg)

    try:
        with smtplib.SMTP(smtp_server, port) as server:
            server.starttls()
            server.login(mail_user, mail_user_pwd)
            server.send_message(email)
            print(f"Email envoyé à {mail_receiver}!")
    
    except smtplib.SMTPAuthenticationError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except smtplib.SMTPException as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

