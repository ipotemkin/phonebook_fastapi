from pydantic import BaseModel
from typing import Optional
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Phone(Base):
    __tablename__ = "phone"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    phone_number = Column(String)


class PhoneBM(BaseModel):
    id: Optional[int]
    name: str
    phone_number: str

    class Config:
        orm_mode = True


class PhoneUpdateBM(BaseModel):
    name: Optional[str]
    phone_number: Optional[str]

    class Config:
        orm_mode = True
