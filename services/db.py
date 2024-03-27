from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

engine = create_engine(os.environ.get('DB_CONNECTION'))
Session = sessionmaker(bind=engine)
