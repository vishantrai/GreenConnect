from sqlalchemy import create_engine #the engine is like the hotline between your Python code and your database — it talks to your DB and executes SQL under the hood
from sqlalchemy.ext.declarative import declarative_base #provides all the structure, but lets your models party with columns and rows
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:Vish%402323@localhost/GreenConnect'

engine = create_engine(SQLALCHEMY_DATABASE_URL) #here the create engine function is taking the address of database and linking these code and database

SessionLocal = sessionmaker(autocommit = False, autoflush=False, bind=engine)
#the sessionmaker fundtion returns an object, bind tells which database engine to connect
Base = declarative_base()

# dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()