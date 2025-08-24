# this is sqlalchemy models
from sqlalchemy import Column, Integer, Float, Boolean, String, ForeignKey, NUMERIC
from sqlalchemy.sql.expression import null, text
from sqlalchemy.sql.sqltypes import TIMESTAMP
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
    address_line = Column(String, nullable=True)
    locality = Column(String, nullable=False)
    city = Column(String, nullable=False)
    state = Column(String, nullable=False)
    country = Column(String, default="BHARAT")
    pincode = Column(String, nullable=False)
    latitude = Column(NUMERIC(12,6), nullable=False)
    longitude = Column(NUMERIC(12,6), nullable=False)

class Role(Base):
    __tablename__="roles"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    volunteer = Column(Boolean, nullable=False, default=True, server_default=text('true'))
    planter = Column(Boolean, nullable=False, default=False)
    care_taker = Column(Boolean,nullable=False,  default=False)
    donor= Column(Boolean, nullable=False, default=False) #mention on frontend as this is plant donor, equipment donor, labour donor because we dont allow direct money donation
    land_provider= Column(Boolean, nullable=False, default=False) 

class LandDonationPost(Base):
    __tablename__ = "land_donation_post"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False ) 
    donor_type = Column(String, nullable=False )
    mobile_number = Column(String, nullable=False) #mobile should not be unique because one number can be used for multiple posts
    email= Column(String, nullable=True)
    address = Column(String, nullable=False)
    latitude = Column(Float, nullable= False)
    longitude = Column(Float, nullable= False)
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
    image_url = Column(String, nullable=False)
    special_note = Column(String, nullable=False)

class Supporters(Base):
    __tablename__="supporters"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False ) 
    donor_type = Column(String, nullable=False )
    mobile_number = Column(String, nullable=False) #mobile should not be unique because one number can be used for multiple posts
    email= Column(String, nullable=True)

class SaplingDonor(Base):
    __tablename__ = "sapling_donor"

    user_id = Column(Integer, ForeignKey("supporters.id"), primary_key=True)
    tree_type = Column(String, nullable=True)
    quantity = Column(Integer, nullable=True)
    special_note = Column(String, nullable=True)

class EquipmentDonor(Base):

    __tablename__ = "equipment_donor"

    user_id = Column(Integer, ForeignKey("supporters.id"), primary_key=True)
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

    user_id = Column(Integer, ForeignKey("supporters.id"), primary_key=True)
    no_of_people = Column(Integer, nullable=True, default= 5)
    availabilty = Column(TIMESTAMP(timezone=True),nullable=False)

class LogisticHelp(Base):

    __tablename__= "logistic help"
    user_id = Column(Integer, ForeignKey("supporters.id"), primary_key=True)
    mode_of_transport = Column(String, nullable=True)
    max_distance = Column(Integer, nullable=True, default= 10)

#notes
#we cannot define more than one table in one class of the sqlalchemy so for each table create different class