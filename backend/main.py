from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor
import models
from database import Base, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

while True:
    try:
        conn = psycopg2.connect(host='localhost', database = 'GreenConnect', user='postgres', password = 'Vish@2323', cursor_factory = RealDictCursor) #

        cursor=conn.cursor()

        print("connection is successful become happy!")
        break
    except Exception as error:
        print("Connection failed but dont worry it is an exception you can solve it ")
        print("error: ", error)