from typing import Union

from fastapi import FastAPI, Request

from fastapi.staticfiles import StaticFiles

from fastapi.responses import HTMLResponse, FileResponse, JSONResponse

from fastapi.templating import Jinja2Templates

from app.endpoints import company_select

import sqlite3

app = FastAPI()

# con: sqlite3.Connection = None  # type: ignore
# con = sqlite3.connect("PSDMD.db")
# @app.on_event("startup")
# async def startup():
#     global con
#     con = sqlite3.connect("PSDMD.db")




# app.mount("/static", StaticFiles(directory="static", html=True), name="static")

templates = Jinja2Templates(directory="static/templates")

# @app.get("/first", response_class=HTMLResponse)
# async def first(request: Request):
#     users = get_users()
#     return templates.TemplateResponse("item.html", {"request": request, "users": users})



@app.get("/company", response_class=JSONResponse)
def read_companies():
    return company_select()

@app.get("/second")
async def main():
    return FileResponse("static/html/index.html")