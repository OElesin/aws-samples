from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hf-summarize")
async def summarize():
    return {"message": "Hello World"}
