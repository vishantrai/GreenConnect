from fastapi import FastAPI, APIRouter, status, Depends
import schemas, utils, models
from sqlalchemy.orm import Session
from database import get_db


router = APIRouter(
    prefix = "/users", #prefix is that part which will be automatically at every route, like whenever i will be declaring any route it is obvious that the previous one will be posts
    tags=["Users"]
)

User = schemas.UserCreate

@router.post("/", status_code=status.HTTP_201_CREATED, response_model= schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends (get_db) ):

    #hasing the password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict(exclude={"confirm_password"})) #** this is for dictionary unpacking 
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.post("/address", status_code=status.HTTP_201_CREATED) #,response_model= schemas.AddressOut)
def address(address: schemas.Address, db: Session = Depends(get_db)):
    new_address = models.Address(**address.dict())
    db.add(new_address)
    db.commit()
    db.refresh(new_address)

    return ("Address saved")