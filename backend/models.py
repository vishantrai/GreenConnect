# this is sqlalchemy models
from sqlalchemy import Column, Integer, DECIMAL, Boolean, String, ForeignKey, NUMERIC
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
    user_id = Column(Integer, ForeignKey("users.id"))
    address_line = Column(String, nullable=False)
    locality = Column(String, nullable=True)
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




#notes
#we cannot define more than one table in one class of the sqlalchemy so for each table create different class