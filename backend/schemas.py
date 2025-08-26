from pydantic import BaseModel, EmailStr, Field, validator, model_validator
from datetime import datetime
from schemas import *
from typing import Optional, Union
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
    created_at: datetime
    
class UserOut(BaseModel):
    id: int
    name: str
    mobile_no: str
    email: EmailStr

    model_config = {
        "from_attributes": True
    }


class AddressCreate(BaseModel):
    address_line: str
    locality: Optional[str] = None #it is not cumpulsory to enter the locality
    city: str
    state: str
    country: str = "BHARAT"
    pincode: str

    @validator("pincode")
    def validate_pincode(cls, v):
        if not re.fullmatch(r"\d{6}", v):
            raise ValueError("Pincode must be exactly 6 digits")
        return v
    
    latitude: float #this is good but at production level it will create trouble so we should make the latitude longitude validator
    longitude: float #below are the validator

    @validator("latitude")
    def validate_latitude(cls, v):
        if not -90 <= v <= 90:
            raise ValueError("Invalid Latitude")
        return v
    
    @validator("longitude")
    def validate_longitude(cls, v):
        if not -180 <= v <= 180:
            raise ValueError("Invalid Longitude")
        return v
    created_at: datetime

# in case of change in address or update the address this schema should be followed, we are giving the user all the entries pre filled just the entries which user want to change can edit and save 
class AddressUpdate(BaseModel):
    address_line: Optional[str] = None #here the all fields are optional that if user want he can enter new data if not then the user can leave it as it is 
    locality: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    pincode: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    created_at: datetime

class AddressOut(BaseModel):
    id:int
    user : UserOut 
    city: str

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


class RoleOut(BaseModel):
    id: int
    user_id: int

    model_config = {
        "from_attributes": True
    }
# incomplete - to complete this i need to revise auth

class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Creating schemas for the posts
class PostBase(BaseModel):
    name: str #(in future it will be replaced by a option where it features name same as username for now it is manual)
    title: str
    mobile_number: str
    email: Optional[EmailStr] = None
    address: str
    latitude: float
    longitude: float
    post_type: str
    description: str
    image_url: str
    created_at: datetime

# post schemas  
class LandDonor(BaseModel):
    area: float
    area_unit: str
    soil_type: str
    tree_type1: str
    tree_type2: str
    tree_type3: bool #js will convert yes/no to true/false
    ownership_type: str
    publicly_accessible: bool
    road_access: bool
    fencing: bool
    water_source: bool
    

class SaplingDonor(BaseModel):
    tree_type: str
    quantity: int

class EquipmentDonor(BaseModel):
    spades: bool
    quantity1: Optional[int] = None
    shovel: bool
    quantity2: Optional[int] = None
    khurpa: bool
    quantity3: Optional[int] = None
    water_can: bool
    quantity4: Optional[int] = None
    other_equipment: Optional[str] = None #the other equipment should be specified by name and number
    quantityM: Optional[int] = None

class Volunteers(BaseModel):
    no_of_people: Optional[int] = 5
    availability: datetime

class LogisticHelp(BaseModel):
    mode_of_transport: str
    max_distance: Optional[int] = 10 


class TreeCareRequest(BaseModel):
    tree_type: str
    current_condition: Optional[str] = None
    water_need: bool
    fence_need: bool
    pest_control: bool
    physical_damage: bool
    soil_health: str
   
class PostCreate(PostBase): 
# what is happening here
# Here we are combining both the schema like all the posts have some common data which we have saved in the postbase and the specific type post details  
    details: Optional[Union[
                LandDonor,
                EquipmentDonor,
                SaplingDonor,
                LogisticHelp,
                Volunteers,
                TreeCareRequest
            ]]  = None


#response model for the post is for the user who is creating the post, it is not what we are going to show as post("A little confusion")
class PostOut(PostBase):
    id: int
    created_at: datetime
    # updated_at: datetime

    details: Optional[Union[
                LandDonor,
                EquipmentDonor,
                SaplingDonor,
                LogisticHelp,
                Volunteers,
                TreeCareRequest          
                            ]] = None
    
    model_config = {
        "from_attributes": True
        }