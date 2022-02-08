from fastapi import FastAPI, Request, Form, Response
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import pickle


class Question(BaseModel):
    text: str


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/")
async def root():
    return {"message": "Transfer Tracker - AI Powered QnA Bot for Football Transfer News"}


@app.post("/qna-response/")
async def qna_response(question: Question):
    print(question)
    return question


@app.get("/home", response_class=HTMLResponse)
async def summarize(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

