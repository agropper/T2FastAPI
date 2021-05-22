# app/api.py

from fastapi import FastAPI

app = FastAPI()

@app.get("/", tags=["root"])
async def read_root() -> dict:
    return {"message": "Welcome to your blog!."}