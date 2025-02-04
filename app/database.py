from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#Define url pf database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

#Create databse engine for use and control it
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
#Create session for database that will be used in main.py
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#Create instance of declarative base
Base = declarative_base()

