from typing import Union

from fastapi import FastAPI, Request

from fastapi.staticfiles import StaticFiles

from fastapi.responses import HTMLResponse, FileResponse

from fastapi.templating import Jinja2Templates

from app.endpoints import get_users

app = FastAPI()

# app.mount("/static", StaticFiles(directory="static", html=True), name="static")

templates = Jinja2Templates(directory="static/templates")

@app.get("/first", response_class=HTMLResponse)
async def first(request: Request):
    users = get_users()
    return templates.TemplateResponse("item.html", {"request": request, "users": users})

@app.get("/users")
def read_users():
    return get_users()

@app.get("/second")
async def main():
    return FileResponse("static/html/index.html")