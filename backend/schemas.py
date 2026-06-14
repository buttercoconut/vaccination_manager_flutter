"""
Pydantic schemas for API request/response validation.
"""

from datetime import date
from typing import List, Optional

from pydantic import BaseModel, EmailStr

# User schemas
class UserBase(BaseModel):
    name: str
    birth_date: date
    phone: str
    email: EmailStr

class UserCreate(UserBase):
    pass

class UserRead(UserBase):
    id: int

    class Config:
        orm_mode = True

# Vaccine schemas
class VaccineBase(BaseModel):
    name: str
    manufacturer: str
    efficacy: Optional[str] = None

class VaccineCreate(VaccineBase):
    pass

class VaccineRead(VaccineBase):
    id: int

    class Config:
        orm_mode = True

# Vaccination schemas
class VaccinationBase(BaseModel):
    vaccine_id: int
    date: date
    side_effects: Optional[dict] = None

class VaccinationCreate(VaccinationBase):
    pass

class VaccinationRead(VaccinationBase):
    id: int
    user_id: int
    vaccine: VaccineRead

    class Config:
        orm_mode = True

# For list responses
class VaccinationList(BaseModel):
    vaccinations: List[VaccinationRead]
