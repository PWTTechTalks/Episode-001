import requests 
from postgres import Postgres
import dotenv
import os

dotenv.load_dotenv('.env_techtalk_SEC')

req = requests.get(url=f'{os.getenv("WEB_URL")}/files/company_tickers.json')

with open(file='cik_tickers.json',mode='w') as file:
    the_json = req.json()

db = Postgres()
    
# always clear out the table first

db.run(f'truncate table "{os.getenv("PG_SCHEMA")}".company_ticker')

# bad for to just toss away this but ...

[ db.run(  f"""insert  into "{os.getenv("PG_SCHEMA")}".company_ticker(
                cik_str,
                ticker,
                title) 
               values (
                   '{the_json[a]["cik_str"]}',
                   '{the_json[a]["ticker"]}',
                   '{the_json[a]["title"].replace("'","''")}') """ ) 
       for a in the_json]

company_cik :str = db.one(f"""select cik_str from "{os.getenv("PG_SCHEMA")}".company_ticker where ticker = 'AES' """)

print (company_cik.rjust(10,'0'))

req = requests.get(url=f"""{os.getenv("DATA_URL")}/submissions/CIK{company_cik.rjust(10,'0')}.json""")

print (f"""{os.getenv("DATA_URL")}/submissions/CIK{company_cik.rjust(10,'0')}.json""")

with open(file='thedump.json',mode='w') as file:
    json.dump(req.json(),file)










