import requests 
from postgres import Postgres
import dotenv

dotenv.load_dotenv('.env_SEC')

req = requests.get(url='https://www.sec.gov/files/company_tickers.json')

with open(file='cik_tickers.json',mode='w') as file:
    the_json = req.json()

db = Postgres()
    
# always clear out the table first

db.run('truncate table "SEC".company_ticker')

# bad for to just toss away this but ...

[ db.run(  f"""insert  into "SEC".company_ticker(
                cik_str,
                ticker,
                title) 
               values (
                   '{the_json[a]["cik_str"]}',
                   '{the_json[a]["ticker"]}',
                   '{the_json[a]["title"].replace("'","''")}') """ ) 
       for a in the_json]






