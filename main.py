from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from ai.analyzer import analyze_log

# Define structure of the request body (payload)
class LogBody(BaseModel):
    text: str

# Create the FastAPI application
app = FastAPI()

# Define the API endpoint
@app.post("/analyzer")
# Call the analyzer function with the provided log text
def analyze(log: LogBody):
    response = analyze_log(log.text)
    return response
