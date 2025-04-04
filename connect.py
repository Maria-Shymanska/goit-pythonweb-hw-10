from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

DB_URL = "postgresql+asyncpg://postgres:fe312@localhost:5432/contacts"

engine = create_engine(DB_URL, echo=False)

Session = sessionmaker(bind=engine)

session = Session()