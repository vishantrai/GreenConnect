from fastapi import APIRouter, status, Depends, HTTPException
import utils, models
from sqlalchemy.orm import Session
from database import get_db
from schemas import UserCreate,UserOut, AddressCreate, AddressOut, AddressUpdate


router = APIRouter(
    prefix = "/users", #prefix is that part which will be automatically at every route, like whenever i will be declaring any route it is obvious that the previous one will be posts
    tags=["Users"]
)


#this is for the user create, mainly it is used at the place of registration of user
@router.post("/register", status_code=status.HTTP_201_CREATED, response_model= UserOut)
def create_user(user: UserCreate, db: Session = Depends (get_db) ):

    #hasing the password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict(exclude={"confirm_password"})) #** this is for dictionary unpacking 
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

# users get operation - each user has access to its profile info 
@router.get("/{user_id}", status_code=status.HTTP_200_OK, response_model=UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    return user


#this is for the address storing of that user, the frontend has to take the returned id and run this route to enter the address, one user can save more than one address 
@router.post("/{user_id}/address", status_code=status.HTTP_201_CREATED ,response_model= AddressOut)
def address(user_id: int, address: AddressCreate, db: Session = Depends(get_db)):
    new_address = models.Address(user_id = user_id, **address.dict())
    db.add(new_address)
    db.commit()
    db.refresh(new_address)

    return new_address 



# address update, - first we need to fetch the user detail then the addresses saved, there can be multiple address so we need to take the address id and then update option will be enabled 
@router.patch("/{user_id}/address/{address_id}", status_code=status.HTTP_201_CREATED, response_model=AddressOut)
def addressUpdate(user_id:int, address_id: int, address_update: AddressUpdate, db: Session = Depends(get_db)):
    #-> user check
    # let first check that the user_id sent is valid or not, weather there is any user exist or not for this id
    user = db.query(models.User).filter(models.User.id == user_id).first() #here we are querying in the database 
    
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    
    #-> address check
    db_address = db.query(models.Address).filter(models.Address.id == address_id, models.Address.user_id == user_id).first() #function me ek address id hai woh id address table me hai ya nhi iske liye yeh code likha "Address.id == address_id" and first() to get the first value
    
    if not db_address:
        raise HTTPException(status_code=404, detail="Address not found for this user")
    
    # the below code is new explained below
    update_data = address_update.dict(exclude_unset = True)
    for key, value in update_data.items():
        setattr(db_address, key, value)
    
    db.commit()
    db.refresh(db_address)
    return db_address


# delete address 
@router.delete("/{user_id}/address/{address_id}", status_code=status.HTTP_200_OK) #HTTP_204_NO_CONTENT - return nothing so whenever you are thinking to return something avoid using this http status code
def address_deleted(user_id: int, address_id: int, db: Session = Depends(get_db)):

    #checking the user id is valid or not
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    
    #checking the address id is valid or not
    address = db.query(models.Address).filter(models.Address.id == address_id, models.Address.user_id == user_id).first()
    if not address:
        raise HTTPException(status_code=404, detail="address not found")

    # delete the address
    db.delete(address)
    db.commit()
    return {"message": "Your address is deleted successfully"}






#NOTES
#update_data = address_update.dict(exclude_unset = True)
    # for key, value in update_data.items():
    #     setattr(db_address, key, value)
# the above code is for updating the address which user already saved
# update_data is a dictionary which is going to update
# here in the first line we are fetching the address schema in the dictionary form and then excluding all that fields which are not edited by the user and looking only the edited fields
# second line the loop is running only in the edited fields 
# last line has a function setattr which is a in-built function which sets an attribute dynamically, syntax - setattr(obj, attr_name, value)