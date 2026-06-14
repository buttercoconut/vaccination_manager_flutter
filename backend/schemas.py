"""
Pydantic schemas for request/response validation.
"""

from datetime import date
from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field

class SideEffectBase(BaseModel):
    description: str

class SideEffectCreate(SideEffectBase):
    pass

class SideEffect(SideEffectBase):
    id: int

    class Config:
        orm_mode = True

class VaccineBase(BaseModel):
    name: str
    manufacturer: Optional[str] = None
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
    side_effect_ids: Optional[List[int]] = Field(default_factory=list)

class VaccinationCreate(VaccinationBase):
    pass

class Vaccination(VaccinationBase):
    id: int
    user_id: int
    vaccine: Vaccine
    side_effects: List[SideEffect] = []

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    name: str
    birth_date: date
    phone: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    vaccinations: List[Vaccination] = []

    class Config:
        orm_mode = True
