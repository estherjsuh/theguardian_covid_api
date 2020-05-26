import requests
from config import API_KEY

r = requests.get("https://content.guardianapis.com/search?q=corona|covid&api-key={}".format(API_KEY)).json()


print(r)
