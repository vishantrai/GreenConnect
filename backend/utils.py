# This is utility file which contain some helping code for other files
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")

# this will store your password only after the hashing so that in case of sql injection or database leak the details of users remain secured
def hash(password: str):
    return pwd_context.hash(password) #Hashes/encrypts a plain text password

#this for login verification
def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password) #Compares plain text password after hashing with hashed password

