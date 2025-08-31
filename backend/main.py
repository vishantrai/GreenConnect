from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor
import models
from database import Base, engine
import routers.user as user, routers.posts as posts, routers.auth as auth, routers.like as like
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

app.include_router(user.router)
app.include_router(posts.router)
app.include_router(auth.router)
app.include_router(like.router)