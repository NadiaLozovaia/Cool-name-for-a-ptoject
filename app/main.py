from typing import Union

from fastapi import FastAPI

from fastapi.staticfiles import StaticFiles


app = FastAPI()

app.mount("/", StaticFiles(directory="static/html", html=True), name="static")


