"""
Pydantic schemas for request/response validation.
"""

from datetime import date
from typing import List, Optional
from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    name: str
    birth_date: date
    phone: str
    email: EmailStr

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int

    class Config:
        orm_mode = True

class VaccineBase(BaseModel):
    name: str
    manufacturer: str
    efficacy: Optional[str] = None

class VaccineCreate(VaccineBase):
    pass

class Vaccine(VaccineBase):
    id: int

    class Config:
        orm_mode = True

class VaccinationBase(BaseModel):
    vaccine_id: int
    date: date
    side_effects: Optional[List[str]] = None

class VaccinationCreate(VaccinationBase):
    user_id: int

class Vaccination(VaccinationBase):
    id: int
    user_id: int
    vaccine: Vaccine

    class Config:
        orm_mode = True
