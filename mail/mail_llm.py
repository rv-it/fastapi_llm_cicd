import smtplib
from email.message import EmailMessage
import os
from fastapi import HTTPException

# Function to send an email
def send_email(response_llm: str, smtp_server: str, port: int, mail_sender: str, mail_receiver: str):
    # Retrieve the sender's email password from environment variables
    mail_sender_pwd = os.getenv("app_pwd_user")
    # Email content (LLM response or error message)
    content_msg = response_llm
    # Create a new EmailMessage object
    email = EmailMessage()
    # Set email headers
    email["From"] = mail_sender
    email["To"] = mail_receiver
    email["Subject"] = "Issue(s) report journalctl" 
    # Add the email body as HTML content
    email.add_alternative(content_msg, subtype="html")

    try:
        # Open a connection to the SMTP server with TLS encryption
        with smtplib.SMTP(smtp_server, port) as server:
            server.starttls()
            server.login(mail_sender, mail_sender_pwd)
            # send the mail
            server.send_message(email)
            return f"Email send to {mail_receiver}."
        
    # Catch SMTP exception and raises FastApI Exception with LiteLLM Exception message
    except smtplib.SMTPAuthenticationError as e:
        raise HTTPException(status_code=401, detail=str(e))
    
    except smtplib.SMTPException as e:
        raise HTTPException(status_code=500, detail=str(e))
    # Catch any other exception
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
