# %% [markdown]
# <!-- @format -->
# 
# #### Do all the imports
# 

# %%
import requests   # for getting the web data
from dotenv import load_dotenv   # for dealing with secrets and environment variables
from os import getenv  # more environment variable stuff
from json import dump  # 


# %% [markdown]
# <!-- @format -->
# 
# #### load the environments and a variable or two
# 

# %%
load_dotenv("techtalk_SEC.secrets")   # userids and passwords and api keys and so forth
load_dotenv("techtalk_SEC.env")    # miscellaneous setup stuff that isn't actually secret

ticker_symbol = "JPM-PD"   # Because everyone loves Jamie Dimon

# %% [markdown]
# <!-- @format -->
# 
# #### put all the pieces of the api call together
# 

# %%
r = requests.Request(
    method="GET",
    url=f'{getenv("WEB_URL")}/files/company_tickers.json',
    headers={
        "User-Agent": getenv("SEC-User-Agent"),        # We hide the user agent so that bots don't scrape and misuse it
        "Accept": "application/json",
    },
)

# %% [markdown]
# <!-- @format -->
# 
# #### Go get the data
# 

# %%
s = requests.Session()

req = s.send(r.prepare())

# %% [markdown]
# <!-- @format -->
# 
# ##### Save the response to an external file
# ##### Completely optional but I like to have a file around to see the stucture of the data
# 

# %%
with open(file="cik_tickers.json", mode="w") as file:
    dump(req.json(), file)

# %% [markdown]
# #### stash the ticker mapping into a couple of dicts for later
# 

# %%
the_json = req.json()
ticker_cik = {the_json[a]["ticker"]: str(the_json[a]["cik_str"]).zfill(10) for a in the_json}
cik_ticker = {str(the_json[a]["cik_str"]).zfill(10): the_json[a]["ticker"] for a in the_json}

# %% [markdown]
# <!-- @format -->
# 
# #### Pull your favorite company's CIK from the dictionary 

# %%
ticker_symbol = "JPM-PD"   # Because everyone loves Jamie Dimon

company_cik = ticker_cik[ticker_symbol]

# %% [markdown]
# <!-- @format -->
# 
# #### And go get the list of "recent" submissions for that company
# 

# %%
r.url = f"""{getenv("DATA_URL")}/api/xbrl/companyfacts/CIK{company_cik}.json""" 

req = s.send(r.prepare())

# %% [markdown]
# <!-- @format -->
# 
# #### Save the results to a file again
# 

# %%
with open(file=f"company-facts-{ticker_symbol}.json", mode="w") as file:
    dump(req.json(), file)

# %% [markdown]
# 
# 
# #### save all of the facts to a dict for later use
# 

# %%
company_facts: dict = req.json()


# %% [markdown]
# ##### You are now ready to spelunk through the financial results of your favorite publically traded company! 


