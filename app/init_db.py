import json
import sqlite3
import datetime
import requests
import shutil
import zipfile
from datetime import date
import os

today = date.today().strftime('%Y%m%d')


def download_psdmd_file(date_str):

    url = f'https://euclid.eba.europa.eu/register/downloads/PSDMD/{date_str}/download-PSDMD-{date_str}0800.zip'

    archive_name = f'download/download-PSDMD-{date_str}.zip'

    local_filename = archive_name
    with requests.get(url, stream=True) as r:
        with open(local_filename, 'wb') as f:
            shutil.copyfileobj(r.raw, f)

    with zipfile.ZipFile(archive_name, 'r') as zip_ref:
        zip_ref.extractall('download/')


def cleanup(date_str):

    folder = 'download'
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        if date_str not in filename:
            os.remove(file_path)


def init_db(date_str):

    con = sqlite3.connect("PSDMD.db")
    cur = con.cursor()
    cur.execute("DROP TABLE if exists PSDMD")
    cur.execute("CREATE TABLE PSDMD (id INT, reference_code INT, company_name_first TEXT, company_name_second TEXT, country TEXT, services_country TEXT, up_date DATE)")

    data = json.load(open(f"download/download-PSDMD-{date_str}0800.json"))
    companies = []

    for index, company in enumerate(data[1]):
        if "Properties" not in company:
            continue
        reference_code = get_property_by_key(
            company["Properties"], "ENT_NAT_REF_COD")
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
            [index, reference_code, company_name_first, company_name_second, country, s, date_str])

    cur.executemany(
        'INSERT INTO PSDMD (id, reference_code, company_name_first, company_name_second, country, services_country, up_date) values (?, ?, ?, ?, ?, ?, ?)', companies)
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


if __name__ == "__main__":
    download_psdmd_file(today)
    cleanup(today)
    init_db(today)

