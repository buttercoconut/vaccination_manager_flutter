from pydantic import BaseModel, Field, EmailStr
from datetime import date
from typing import List, Optional, Dict

class UserBase(BaseModel):
    name: str
    birth_date: date
    phone: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: int
    class Config:
        orm_mode = True

class VaccineBase(BaseModel):
    name: str
    manufacturer: str
    efficacy: Optional[str] = None
    interval_days: int

class VaccineCreate(VaccineBase):
    pass

class VaccineOut(VaccineBase):
    id: int
    class Config:
        orm_mode = True

class VaccinationBase(BaseModel):
    vaccine_id: int
    date: date
    side_effects: Optional[Dict[str, str]] = Field(default_factory=dict)

class VaccinationCreate(VaccinationBase):
    pass

class VaccinationOut(VaccinationBase):
    id: int
    user_id: int
    vaccine: VaccineOut
    class Config:
        orm_mode = True
