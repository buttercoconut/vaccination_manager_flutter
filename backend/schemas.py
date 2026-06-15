"""Pydantic schemas for request/response validation."""

from datetime import date
from typing import List, Optional
from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    name: str
    birth_date: date
    phone: Optional[str] = None
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: int

    class Config:
        orm_mode = True

class VaccineBase(BaseModel):
    name: str
    manufacturer: Optional[str] = None
    efficacy: Optional[str] = None

class VaccineCreate(VaccineBase):
    pass

class VaccineOut(VaccineBase):
    id: int

    class Config:
        orm_mode = True

class VaccinationBase(BaseModel):
    vaccine_id: int
    date: date
    side_effects: Optional[List[str]] = None

class VaccinationCreate(VaccinationBase):
    pass

class VaccinationOut(VaccinationBase):
    id: int
    user_id: int
    vaccine: VaccineOut

    class Config:
        orm_mode = True
