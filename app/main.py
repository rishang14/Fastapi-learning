from fastapi import FastAPI, Query
from fastapi.responses import PlainTextResponse
import yaml
import tempfile
from typing import Literal

app = FastAPI()

@app.get("/") 
async def root():
    return {"message": "Hello"}