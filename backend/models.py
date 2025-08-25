# this is sqlalchemy models
from sqlalchemy import Column, Integer, Float, Boolean, String, ForeignKey, NUMERIC
from sqlalchemy.sql.expression import null, text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship
import psycopg2
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    mobile_no = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String,nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),nullable=False, server_default=text('now()'))

class Address(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User") 
    address_line = Column(String, nullable=True)
    locality = Column(String, nullable=False)
    city = Column(String, nullable=False)
    state = Column(String, nullable=False)
    country = Column(String, default="BHARAT")
    pincode = Column(String, nullable=False)
    latitude = Column(NUMERIC(12,6), nullable=False)
    longitude = Column(NUMERIC(12,6), nullable=False)
    created_at=Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

class Role(Base):
    __tablename__="roles"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    volunteer = Column(Boolean, nullable=False, default=True, server_default=text('true'))
    planter = Column(Boolean, nullable=False, default=False)
    care_taker = Column(Boolean,nullable=False,  default=False)
    donor= Column(Boolean, nullable=False, default=False) #mention on frontend as this is plant donor, equipment donor, labour donor because we dont allow direct money donation
    land_provider= Column(Boolean, nullable=False, default=False) 

# post tables
class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False ) 
    title = Column(String, nullable=False)
    mobile_number = Column(String, nullable=False) #mobile should not be unique because one number can be used for multiple posts
    email= Column(String, nullable=True)
    address = Column(String, nullable=False)
    latitude = Column(Float, nullable= False)
    longitude = Column(Float, nullable= False)
    post_type = Column(String, nullable = False) 
    description = Column(String, nullable=False)
    image_url = Column(String, nullable=False)
    created_at=Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

class LandDonationPost(Base):
    __tablename__ = "land_donations"

    id = Column(Integer, ForeignKey("posts.id"), primary_key=True)
    area = Column(Float, nullable=False)
    area_unit = Column(String, nullable=False)
    soil_type = Column(String, nullable=False)
    tree_type1 = Column(String, nullable=False)
    tree_type2 = Column(String, nullable=False)
    tree_type3 = Column(Boolean, nullable=False)
    ownership_type = Column(String, nullable=False)
    publicly_accessible = Column(Boolean, nullable=False)
    road_access = Column(Boolean, nullable=False)
    fencing = Column(Boolean, nullable=False)
    water_source = Column(Boolean, nullable=False)


class SaplingDonor(Base):
    __tablename__ = "sapling_donor"

    id = Column(Integer, ForeignKey("posts.id"), primary_key=True)
    tree_type = Column(String, nullable=True)
    quantity = Column(Integer, nullable=True)


class EquipmentDonor(Base):

    __tablename__ = "equipment_donor"

    id = Column(Integer, ForeignKey("posts.id"), primary_key=True)
    spades = Column(Boolean, nullable=True)
    equipment_num1 = Column(Integer, nullable=True)

    shovel = Column(Boolean, nullable=True)
    equipment_num2 = Column(Integer, nullable=True)

    khurpa = Column(Boolean, nullable=True)
    equipment_num3 = Column(Integer, nullable=True)

    water_can = Column(Boolean, nullable=True)
    equipment_num4 = Column(Integer, nullable=True)

    other_equipment = Column(String, nullable=True)
    other_equipment_number = Column(Integer, nullable=True)

class LabourDonor(Base):
    __tablename__ = "labour_donor " 

    id = Column(Integer, ForeignKey("posts.id"), primary_key=True)
    no_of_people = Column(Integer, nullable=True, default= 5)
    availabilty = Column(TIMESTAMP(timezone=True),nullable=False)

class LogisticHelp(Base):
    __tablename__= "logistic help"

    id = Column(Integer, ForeignKey("posts.id"), primary_key=True)
    mode_of_transport = Column(String, nullable=True)
    max_distance = Column(Integer, nullable=True, default= 10)

class CareRequests(Base):
    __tablename__ = "care_requests"

    id = Column(Integer, ForeignKey("posts.id"), primary_key=True)
    tree_type = Column(String, nullable=False)
    current_condition = Column(String, nullable=False)
    water_need = Column(Boolean)
    fence_need = Column(Boolean)
    pest_control = Column(Boolean)
    physical_damage = Column(Boolean)
    soil_health = Column(String)


#notes
#we cannot define more than one table in one class of the sqlalchemy so for each table create different class