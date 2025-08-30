from jose import JWTError, jwt #the jose is used for creating the token 
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer #This endpoint needs a token, and that token must be sent in the Authorization header as a Bearer token.
from datetime import datetime, timedelta
import schemas
from config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login') #here we will be giving a token which can be used by the user for autorization and identify the true user, tokenUrl is the URL where client can get the token

#to create a token we need 3 things - secret_key, algorithm, expriation time, secret key is the most important part of authorization it should not be hardcoded like here(later we will make it env variable)

# SECRET_KEY = "23sdbv5wnebf767fbdhsbi89dnsbdhg634bbsdhf532bvg43b5v3g3"
# ALGORITHM = "HS256" #you can know more algo from google
# ACCESS_TOKEN_EXPIRE_MINUTES =30 #ek baar logged user kb tk logged rhega
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


def create_access_token(data: dict): #this is a jwt token factory, each time client login a token is created
    to_encode = data.copy() #just making a copy of data
    expire = datetime.utcnow() + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire}) #token ki valisity kitne time tk hai, kb tk user logged in rhega
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt #returning the token which can be used by the client

# this is the token checker - yahi se pta chalega ki tujhe access milega ya nhi
def verify_access_token(token: str, credential_exceptions): #the token is shared and credential_exceptions → a prebuilt HTTPException (like 401 Unauthorized) to throw if the token fails.
    try:
        decoded_jwt = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]) #here we are decoding the token by the secret key, and the algo which was used to create the token
        id: str = decoded_jwt.get("user_id") # 

        if id is None: #if we dont get the user_id in the token then we will raise error
            raise credential_exceptions
        token_data = schemas.TokenData(id=id) #if token is verified mtlb user_id me id mil gya then token data naam ka ek object me id return kr rhe

    except JWTError: #if any error ocurred during the decoding then return this error
        raise credential_exceptions
    
    return token_data #sb thik rha tb token ka data returned


# this function is to give data to the "authenticated user"
def get_current_user(token: str = Depends(oauth2_scheme)): # this is a dependency function which uses Depends(), this token: str = Depends(oauth2_scheme) automatically HTTP request ke header se bearer token ko pick krega 
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="could not validate credentials", headers={"WWW-Authenticate": "Bearer"}) # if the token is invalid then error raised 

    return verify_access_token(token, credentials_exception)  #calling the verify_access_token function  