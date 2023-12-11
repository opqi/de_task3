from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
import os
from dotenv import load_dotenv
from pathlib import Path


dotenv_path = Path('./postgres/.env_postgres')
load_dotenv(dotenv_path=dotenv_path)

host = 'localhost'
username = os.getenv('POSTGRES_USER')
password = os.getenv('POSTGRES_PASSWORD')
db = os.getenv('POSTGRES_DB')

engine = create_engine(
    f'postgresql://{username}:{password}@{host}/{db}')

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
