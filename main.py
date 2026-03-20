from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from ai.analyzer import analyze_log
from mail.mail_llm import send_email

# Define structure of the request body (/analyzer payload)
class LogBody(BaseModel):
    text: str
    model: str

# Define structure of the request body (/mail payload)
class MailBody(BaseModel):
    content: str
    smtp_srv : str
    port: int
    sender: str
    receiver: str


# Create the FastAPI application
app = FastAPI()

# Define the API endpoint
@app.post("/analyzer")
# Call the analyze function with the provided log text and model
def analyze(log: LogBody):
    response = analyze_log(log.text, log.model)
    return response

# Define the API endpoint
@app.post("/mail")
# Call the mail function with provided settings
def mail(mail: MailBody):
    response = send_email(mail.content, mail.smtp_srv, mail.port, mail.sender, mail.receiver)
    return response
