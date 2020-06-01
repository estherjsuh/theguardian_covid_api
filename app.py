import requests
from config import API_KEY

params ={
    "api-key" : API_KEY,
    "order-by" : "newest",
    "page-size" : 200}

url = "https://content.guardianapis.com/search?q=coronavirus|covid"

def get_meta_data():
    r = requests.get(url, params)
    return r.json()

r= get_meta_data()
total_pages = r["response"]["pages"]

results = []

for current_page in range(1, total_pages+1):
    params['page'] = current_page
    resp = requests.get(url, params)
    data = resp.json()
    results.extend(data['response']['results'])
    current_page +=1


# for i in results:
#     print(i['webPublicationDate'],i['webTitle'], i['webUrl'])
