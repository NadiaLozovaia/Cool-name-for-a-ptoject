import json
import sqlite3
import datetime
import requests
import shutil
import zipfile
from datetime import date
import os

today = date.today().strftime('%Y%m%d')
con = sqlite3.connect("PSDMD.db")


def download_psdmd_file(date_str):

    url = f'https://euclid.eba.europa.eu/register/downloads/PSDMD/{date_str}/download-PSDMD-{date_str}0000.zip'

    archive_name = f'download/download-PSDMD-{date_str}.zip'

    local_filename = archive_name
    with requests.get(url, stream=True) as r:
        with open(local_filename, 'wb') as f:
            shutil.copyfileobj(r.raw, f)

    with zipfile.ZipFile(archive_name, 'r') as zip_ref:
        zip_ref.extractall('download/')


def cleanup_file(date_str):

    folder = 'download'
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        if date_str not in filename:
            os.remove(file_path)


def parse_companies(date_str):
    data = json.load(open(f"download/download-PSDMD-{date_str}0000.json"))
    companies = []

    for company in data[1]:
        if "Properties" not in company:
            continue
        reference_code = get_property_by_key(
            company["Properties"], "ENT_NAT_REF_COD")
        if not reference_code: 
            continue
        
        company_names = get_property_by_key(company["Properties"], "ENT_NAM")
        company_name_first, company_name_second = company_name_check(
            company_names)
        country = get_property_by_key(company["Properties"], "ENT_COU_RES")
        services_country = []
        s = ''
        if "Services" not in company:
            continue

        for service in company["Services"]:
            for item in service:
                services_country.append(item)
        s = ', '.join(services_country)
        companies.append(
            [reference_code, company_name_first, company_name_second, country, s, date_str])
    return companies


def init_db(date_str):

    cur = con.cursor()
    cur.execute("DROP TABLE if exists PSDMD")
    cur.execute('''
        CREATE TABLE  PSDMD (
            id integer primary key, 
            reference_code TEXT required, 
            company_name_first TEXT, 
            company_name_second TEXT, 
            country TEXT, 
            services_country TEXT, 
            up_date DATE 
            )'''
                )
# UNIQUE(reference_code, country)
    companies = parse_companies(date_str)

    res = cur.executemany(
        '''INSERT INTO PSDMD (
            reference_code, 
            company_name_first, 
            company_name_second, 
            country, 
            services_country, up_date) 
            values (?, ?, ?, ?, ?, ?)''', companies
    )
    con.commit()
    print(res.fetchall())

def update_db(date_str):

    cur = con.cursor()
    companies = parse_companies(date_str)
    new_com = []
    for item in companies:
        new_com.append([item[4], item[5], item[0], item[3]])
    cur.executemany(
        "UPDATE PSDMD SET services_country = ? and up_date = ? WHERE reference_code = ?  and country = ?", new_com)

    # 'INSERT INTO PSDMD (id, reference_code, company_name_first, company_name_second, country, services_country, up_date) values (?, ?, ?, ?, ?, ?, ?)', companies)


def cleanup_db(date_str):
    cur = con.cursor()
    res = cur.execute("DELETE FROM PSDMD WHERE up_date != ?", (date_str,))
    print(res.fetchone())


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


if __name__ == "__main__":
    download_psdmd_file(today)
    cleanup_file(today)
    init_db(today)
    # update_db(today)
    # cleanup_db(today)
