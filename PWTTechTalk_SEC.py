# %% [markdown]
# <!-- @format -->
# 
# #### Do all the imports
# 

# %%
import requests 
from postgres import Postgres
import dotenv
import os
from json import dump

# %% [markdown]
# <!-- @format -->
# 
# #### load the environments
# 

# %%
dotenv.load_dotenv('techtalk_SEC.secrets')
dotenv.load_dotenv('techtalk_SEC.env')

# %% [markdown]
# <!-- @format -->
# 
# #### prepare the request
# 

# %%


SEC_headers= {
    "User-Agent":"PWTTechTalkBot/1.0 Port Wallis Technologies contact - rwolfe@portwallistechnologies.com",
    "Accept":"application/json"
} 

the_url = f'{os.getenv("WEB_URL")}/files/company_tickers.json'

r= requests.Request(method='GET',url=the_url,headers=SEC_headers)
s = requests.Session()

# %% [markdown]
# <!-- @format -->
# 
# #### Go get the data
# 

# %%

req= s.send( r.prepare())

# %% [markdown]
# <!-- @format -->
# 
# #### Save the response to an external file (completely optional)
# 

# %%
with open(file='cik_tickers.json',mode='w') as file:
    dump(req.json(),file)   

# %% [markdown]
# <!-- @format -->
# 
# #### Stash the response data in a variable
# 

# %%
the_json = req.json()

# %% [markdown]
# <!-- @format -->
# 
# #### Stash the response in a database table
# 
# 1. create the connection
# 1. clear out the table
# 1. insert the new data
# 

# %%
db = Postgres()
    
# always clear out the table first

db.run(f'truncate table "{os.getenv("PG_SCHEMA")}".company_ticker')

# bad for us to just toss away this but ...

a = [ db.run(  f"""insert  into "{os.getenv("PG_SCHEMA")}".company_ticker(
                cik_str,
                ticker,
                title) 
               values (
                   '{the_json[a]["cik_str"]}',
                   '{the_json[a]["ticker"]}',
                   '{the_json[a]["title"].replace("'","''")}') """ ) 
       for a in the_json]

# %% [markdown]
# <!-- @format -->
# 
# #### Pull your favorite company's CIK from the database table
# 

# %%
ticker_symbol = 'AES'

company_cik :str = db.one(f"""select cik_str from 
                          "{os.getenv("PG_SCHEMA")}".company_ticker where ticker = '{ticker_symbol}' """)

# CIK has to be 0 padded to 10 digits with leading 0's or it just honks 

company_cik = company_cik.rjust(10,'0')

# %% [markdown]
# <!-- @format -->
# 
# #### And go get the list of recent submissions for that company
# 

# %%

the_url = f"""{os.getenv("DATA_URL")}/submissions/CIK{company_cik}.json"""

r.url = the_url

req= s.send( r.prepare())

# %% [markdown]
# <!-- @format -->
# 
# #### Save the results to a file again
# 

# %%
with open(file=f'submissions-{ticker_symbol}.json',mode='w') as file:
    dump(req.json(),file)

# %% [markdown]
# <!-- @format -->
# 
# #### save the submissions to a couple of dicts for later use
# 

# %%

submissions:dict = req.json()

recent_filings:dict = submissions["filings"]["recent"]

submission_count =  len(recent_filings["accessionNumber"])

sub_list = []

for i in range(submission_count):
    sub_list.append( {k: recent_filings[k][i] for k in recent_filings.keys()})



# %%
form_names = set()

[
    form_names.add(sub_list[i]["form"])
    for i in range(len(sub_list))
    if sub_list[i]["form"] not in form_names
]

all_forms:dict[str:list] = {k:list() for k in form_names}


[
    all_forms[sub_list[i]["form"]].append(sub_list[i]) 
    for i in range(submission_count) 
]



