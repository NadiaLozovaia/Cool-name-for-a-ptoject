import json
import sqlite3

def init_db():

    con = sqlite3.connect("PSDMD.db")
    cur = con.cursor()
    cur.execute("DROP TABLE if exists PSDMD")
    cur.execute("CREATE TABLE PSDMD (id INT, reference_code INT, company_name_first TEXT, company_name_second TEXT, country TEXT)")

    data = json.load(open("download-PSDMD-202302280800.json"))
    companies = []
    for index, company in enumerate(data[1]):
        if "Properties" not in company:
            continue
        reference_code = get_property_by_key(
            company["Properties"], "ENT_NAT_REF_COD")
        company_names = get_property_by_key(company["Properties"], "ENT_NAM")
        company_name_first, company_name_second = company_name_check(company_names)
        country = get_property_by_key(company["Properties"], "ENT_COU_RES")

        companies.append(
            [index, reference_code, company_name_first, company_name_second, country])
    cur.executemany(
        'INSERT INTO PSDMD (id, reference_code, company_name_first, company_name_second, country) values (?, ?, ?, ?, ?)', companies)
    con.commit()

def get_property_by_key(properties, key):
    for property in properties:
        if key in property:
            return property[key]
    return None


def company_name_check(company_names: list[str] | str) -> tuple[str, str]:
    if isinstance(company_names, str):
        return company_names, None
    if company_names[1].isascii():
        return company_names[1], company_names[0]
    return company_names[0], company_names[1]

if __name__== "__main__":
    init_db()


