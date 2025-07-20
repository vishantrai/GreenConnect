from pydantic import BaseModel, EmailStr, Field, validator, model_validator
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
    confirm_password: str
    @validator("password") #Hey! Before you accept a value for the password field, run this function first
    def validate_password(cls, v): #cls refers to the Pydantic model class itself and v is the value of password which needs validation 
        if not re.match("^[A-Za-z0-9]+$", v): #^ indicates the start of string
            raise ValueError("Password must contain only letters and numbers (no symbols)")
        if not re.search("[a-zA-Z]", v):
            raise ValueError("Password must contain at least one letter")
        if not re.search("[0-9]", v):
            raise ValueError("Password must contain at least one number")
        return v #If all checks pass, the value is returned (aka accepted and used in the model)
    # created_at: datetime

    @model_validator(mode="after") #root validator validates that the password == confirm password as the user have to give both on the frontend
    def passwords_match(self):
        if self.password != self.confirm_password:
            raise ValueError("Password and Confirm Password do not match ")
        return self 
    model_config = {
        "from_attributes": True
    }
    
class UserOut(BaseModel):
    id: int
    name: str
    created_at: datetime

    model_config = {
        "from_attributes": True
    }


class Address(BaseModel):
    user_id: int
    address_line: str
    locality: Optional[str] #it is not cumpulsory to enter the locality
    city: str
    state: str
    country: str = "BHARAT"
    pincode: str
    @validator("pincode")
    def validate_pincode(cls, v):
        if not re.fullmatch(r"\d{6}", v):
            raise ValueError("Pincode must be exactly 6 digits")
        return v
    latitude: float
    longitude: float

class AddressOut(BaseModel):
    id:int
    # name: str
    address_line: str

    model_config = {
        "from_attributes": True
    }

class Role(BaseModel):
    user_id: int
    volunteer: bool = True
    planter: bool = False
    care_taker: bool = False
    donor: bool = False
    land_provider : bool = False
#this is not completed there is a few more thing to do so before moving forward just learn about because these things i dont understand when i was learning fastapi from tutorial

class RoleOut(BaseModel):
    id: int
    user_id: int

    class Config:
        orm_mode = True
 

