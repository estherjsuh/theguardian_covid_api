import requests
from config import API_KEY, pw
import pandas as pd
import psycopg2

conn = psycopg2.connect(database='covid', user='esther', password=pw, host='localhost', port='5432')
cur = conn.cursor()
cur.execute("""
CREATE TABLE covid
(article_id VARCHAR PRIMARY KEY,
publication_date VARCHAR,
title VARCHAR,
web_url VARCHAR,
section VARCHAR);
""")


params ={
    "api-key" : API_KEY,
    "order-by" : "newest",
    "page-size" : 200}

url = "https://content.guardianapis.com/search?q=coronavirus|covid"

def get_meta_data():
    r = requests.get(url, params)
    return r.json()

r = get_meta_data()
total_pages = r["response"]["pages"]

results = []

for current_page in range(1,total_pages+1):
    params['page'] = current_page
    resp = requests.get(url, params)
    data = resp.json()
    results.extend(data['response']['results'])
    current_page +=1


for i in results:
    # import_data = i['id'],i['webPublicationDate'],i['webTitle'], i['webUrl'], i['sectionName']
    try:
        cur.execute("INSERT INTO covid VALUES (%s, %s, %s, %s, %s)",(
        i['id'],i['webPublicationDate'],i['webTitle'], i['webUrl'], i['sectionName']))
    except psycopg2.IntegrityError:
        conn.rollback()
    else:
        conn.commit()

conn.close()
