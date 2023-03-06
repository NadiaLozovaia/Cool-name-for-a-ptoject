import sqlite3


def hello_world():
    return {"Hello": "World"}


def company_select():
    con = sqlite3.connect("PSDMD.db")
    cur = con.cursor()
    res = cur.execute("SELECT * FROM PSDMD LIMIT 3")
    companies_list = res.fetchall()
    companies = []
    for company in companies_list:
        
        company_dict = {"id": company[0],
                        "ref_code": company[1],
                        "name_lat": company[2],
                        "name_second": company[3],
                        "country": company[4]}
        companies.append(company_dict)
    
    return companies
