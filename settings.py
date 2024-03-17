import os
from dotenv import load_dotenv


load_dotenv()

USER=os.getenv('USER')
DATABASE=os.getenv('DATABASE')
DATABASE_URL=os.getenv('DATABASE_URL')