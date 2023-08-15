import requests 
import json
from postgres import Postgre
from dotenv import  get_key

API_KEY:str = get_key(".env","API_KEY")


the_url:str = f'{get_key(".env","BASE_URL")}/petroleum/pri/gnd/data?api_key={API_KEY}'
the_header = {
    "Accept": "Application/json",
    "Content-Type":"Application/json"
}
the_json = {
    "frequency": "weekly",
    "data": [
        "value"
    ],
    "facets": {},
    "start": "2023-07-01"
}

req = requests.post(url=the_url,json=the_json,headers=the_header)

parts:dict = req.json()

print ([a for a in parts['response']['data']])

#print (parts)

#print( [r for r in req.json()["response"]['data']] )

#print( req.json() )







