from fastapi import FastAPI, APIRouter, status, Depends
import schemas, utils, models
from sqlalchemy.orm import Session
from database import get_db


router = APIRouter(
    prefix = "/users", #prefix is that part which will be automatically at every route, like whenever i will be declaring any route it is obvious that the previous one will be posts
    tags=["Users"]
)

User = schemas.UserCreate

@router.post("/", status_code=status.HTTP_201_CREATED, response_model= schemas.UserCreate)
def create_user(user: schemas.UserCreate, db: Session = Depends (get_db) ):

    #hasing the password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict()) #** this is for dictionary unpacking 
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return (f"here are some details {new_user}")