from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import schemas, database, models, utils, oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(
    tags=["Authentication"] #here the authentication is only fot the documentation it doesnt have use in the code
)

@router.post("/login")
# def login(user_credentials: schemas.Login, db: Session = Depends(database.get_db)):
#     user = db.query(models.User).filter(models.User.email == user_credentials.email).first()
    #here in the above code we are encountering a problem which is using the schemas for checking the login details which is not efficient instead we can use oauth2 for this as - 

def login(user_credential: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)): #here the main thing is the OAuth2PasswordRequestForm, it is a class given by fastapi which automatically fills the username and password details 
    user = db.query(models.User).filter(models.User.email == user_credential.username).first() #to test this route send details through form-data under body

    if not user: #here we checked the username is correct or not 
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    if not utils.verify(user_credential.password, user.password): #here we are checking the password is correct or not
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    access_token = oauth2.create_access_token(data={"user_id": user.id}) # this is creating a jwt token 

    return{ #once the client is logged in successfully this details will be returned 
        "access_token": access_token, #We send the token to the client because after login, the server needs a way to remember who you are without asking for your username + password every single time
        "token_type": "bearer" #what is bearer - it is a type of token - This token should be sent in the Authorization header as a Bearer token.
    } #these tokens are stored as cookies

