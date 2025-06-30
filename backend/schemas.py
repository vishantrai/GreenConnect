from pydantic import BaseModel, EmailStr, Field, validator
from datetime import datetime
from typing import Optional
import re #re lets you search, match, extract, and manipulate text

#BaseModel-Hey Pydantic, here’s the kind of data I expect. Validate it, clean it, and throw hands if something's off.

class UserCreate(BaseModel):
    name: str
    mobile_no: str
    email: EmailStr #Emailstr will verify email as it is real or not
    #for defining password we are going to learn some new concept, here we want a password with combination of letters and numbers and min character should be 8
    password: str = Field(..., min_length=8)
    @validator("password") #Hey! Before you accept a value for the password field, run this function first
    def validate_password(cls, v): #cls refers to the Pydantic model class itself and v is the value of password which needs validation 
        if not re.match("^[A-Za-z0-9]+$", v): #^ indicates the start of string
            raise ValueError("Password must contain only letters and numbers (no symbols)")
        if not re.search("[a-zA-Z]", v):
            raise ValueError("Password must contain at least one letter")
        if not re.search("[0-9]", v):
            raise ValueError("Password must contain at least one number")
        return v #If all checks pass, the value is returned (aka accepted and used in the model)
    created_at: datetime