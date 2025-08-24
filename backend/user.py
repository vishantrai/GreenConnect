from fastapi import APIRouter, status, Depends
import schemas, utils, models
from sqlalchemy.orm import Session
from database import get_db


router = APIRouter(
    prefix = "/users", #prefix is that part which will be automatically at every route, like whenever i will be declaring any route it is obvious that the previous one will be posts
    tags=["Users"]
)


#this is for the user create, mainly it is used at the place of registration of user
@router.post("/register", status_code=status.HTTP_201_CREATED, response_model= schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends (get_db) ):

    #hasing the password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict(exclude={"confirm_password"})) #** this is for dictionary unpacking 
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

#this is for the address storing of that user, the frontend has to take the returned id and run this route to enter the address, one user can save more than one address 
@router.post("/{user_id}/address", status_code=status.HTTP_201_CREATED) #,response_model= schemas.AddressOut)
def address(user_id: int, address: schemas.Address, db: Session = Depends(get_db)):
    new_address = models.Address(user_id = user_id, **address.dict())
    db.add(new_address)
    db.commit()
    db.refresh(new_address)

    return new_address.city

# address update, - first we need to fetch the user detail then the addresses saved, there can be multiple address so we need to take the address id and then update option will be enabled 