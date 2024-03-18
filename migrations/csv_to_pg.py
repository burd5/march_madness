import pandas as pd
from sqlalchemy import create_engine
import psycopg2
import os
from frontend.settings import USER,DATABASE

data_file_path = os.listdir('/Users/austinburdette/Documents/Projects/march_madness/data/')

def read_csvs_to_pg(files):
    engine = create_engine(f'postgresql://{USER}@localhost:5432/{DATABASE}')
    for file in files:
        df = pd.read_csv(f'/Users/austinburdette/Documents/Projects/march_madness/data/{file}', sep=',', encoding='latin-1')
        filename = create_file_name(file)
        df.to_sql(filename, engine, if_exists="replace")

def create_file_name(file):
    title = file.split('.csv')[0]
    lower_title = '_'.join(title.split()).lower()
    return f"_{lower_title}" if lower_title.startswith('5') else lower_title