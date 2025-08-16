from sqlalchemy import create_engine, Column,String, integer, Boolean, Float, ForeignKey
from sqlalchemy.orm import declarative_base

# databse connection
db = create_engine("sqlite:///database.db")

# Base class for declarative models
Base = declarative_base()

class User(Base):
  __tablename__ = "users"

  id =
  name = 
  email = 
  password = 
  active = 
  admin = 