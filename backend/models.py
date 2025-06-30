from sqlalchemy import Column, Integer, DECIMAL, Boolean, String, ForeignKey
from sqlalchemy.sql.expression import null, text
from sqlalchemy.sql.sqltypes import TIMESTAMP
import psycopg2
from database import Base

class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullabe=False)
    name = Column(String, nullable=False)
    mobile_no = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String,nullable=False)
    address = Column(String, nullable=False)
    latitude = Column(DECIMAL, nullable=False)
    longitude = Column(DECIMAL, nullable=False)
    Roles = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),nullable=False, server_default=text('now()'))
