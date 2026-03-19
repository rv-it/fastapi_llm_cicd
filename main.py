from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from ai.analyzer import analyze_log
from mail.mail_llm import send_email

# Define structure of the request body (payload)
class LogBody(BaseModel):
    text: str

class MailSettings(BaseModel):
    content: str
    smtp_srv : str
    port: int
    receiver: str


# Create the FastAPI application
app = FastAPI()

# Define the API endpoint
@app.post("/analyzer")
# Call the analyzer function with the provided log text
def analyze(log: LogBody):
    response = analyze_log(log.text)
    return response

@app.post("/mail")
def mail(mail: MailSettings):
    response = send_email(mail.content, mail.smtp_srv, mail.port, mail.receiver)
    return response
