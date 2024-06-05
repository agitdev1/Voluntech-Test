from imports import *
from pydantic import BaseModel, EmailStr

    
class volunteer(BaseModel):
    first_name: str
    last_name: str
    age:int
    gender: str
    email: str
    password: str
    city:str
    skills: list[str]
    cause: list[str]
    gender: str
    volunteer_hrs: str

class organization(BaseModel):
    name: str
    email: str
    city:str
    priorities: list[str]
    cause: list [str]
    orgtype: str
    password: str
    

class ResetToken(BaseModel):
    email: str
    token: str
    expiration_time: datetime

class Email(BaseModel):
    email: str

class ResetToken(BaseModel):
    email: str
    token: str
    expiration_time: datetime

class ResetPasswordData(BaseModel):
    token: str
    new_password: str

class Opportunity(BaseModel):
    organizer: str
    name: str
    description: str
    limit: int
    start_date: datetime
    end_date: datetime
    location: str
    skills: list[str]
    cause: list[str]