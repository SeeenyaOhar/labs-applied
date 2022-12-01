from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("postgresql://postgres:admin@localhost:5432/Online-Classes-Service")
Session = sessionmaker(bind=engine)
