from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from ai.analyzer import analyze_log

class LogBody(BaseModel):
    text: str


app = FastAPI()

@app.post("/analyzer")
def analyze(log: LogBody):
    response = analyze_log(log.text)
    return response
