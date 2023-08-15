from postgres import Postgres, InterfaceError, DataError, ProgrammingError, ConnectionContextManager
from psycopg2 import OperationalError
from dotenv import  get_key, load_dotenv
from os import environ 

load_dotenv(".env")

db_schema = environ.get('PG_SCHEMA')
try : 
     db = Postgres()
except InterfaceError as interface_error:
    print(f' Interface error: {interface_error.pgerror}')
except ProgrammingError as programming_error:
    print(f' Programming error: {programming_error.pgerror}')
except DataError as data_error:
    print(f' Data error: {data_error.pgerror}')
except OperationalError as operational_error:
    print(f' Operational error: {operational_error.args}')
except Exception as another_error:
    print (f'Another Error:{another_error.args}')    
else:
    c:ConnectionContextManager = db.get_connection()
    print(f' Connected')

results = db.all(f'''select * from information_schema.tables s 
                 where s.table_schema='{db_schema}'
       ''')
print (results)
