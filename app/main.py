from typing import Union

from fastapi import FastAPI, Request

from fastapi.staticfiles import StaticFiles

from fastapi.responses import HTMLResponse, FileResponse, JSONResponse

from fastapi.templating import Jinja2Templates

from app.endpoints import company_select, info_company, company_list_country, company_by_ref_code

import sqlite3

app = FastAPI()


# app.mount("/static", StaticFiles(directory="static", html=True), name="static")

templates = Jinja2Templates(directory="static/templates")

# @app.get("/first", response_class=HTMLResponse)
# async def first(request: Request):
#     users = get_users()
#     return templates.TemplateResponse("item.html", {"request": request, "users": users})

@app.get("/companies", response_class=HTMLResponse)
async def companies_list_all(request: Request):
    selected_companies = company_select()
    return templates.TemplateResponse("companies.html", {"request": request, 'companies': selected_companies})

@app.get("/company/{id}", response_class=HTMLResponse)
async def one_company(request: Request, id):
    info = info_company(id)
    return templates.TemplateResponse("one_company.html", {"request": request, 'company': info})

# @app.get("/company", response_class=JSONResponse)
# def read_companies():
#     return company_select()

@app.get("/second")
async def main():
    return FileResponse("static/html/index.html")

@app.get("/api/companies")
async def api_companies_list(country:str):
    companies = company_list_country(country)
    return companies

@app.get("/api/company")
async def api_company_by_ref_code(ref_code:str):
    company = company_by_ref_code(ref_code)
    return company