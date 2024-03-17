import os
from dotenv import load_dotenv


load_dotenv()

USER=os.getenv('USER')
DATABASE=os.getenv('DATABASE')
DATABASE_URL=os.getenv('DATABASE_URL')
KEY=os.getenv('KEY')
URL=os.getenv('URL')
SQL_ACLH_STRING=os.getenv('ALCH_STRING')