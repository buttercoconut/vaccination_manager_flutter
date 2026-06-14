"""
FastAPI routers for users, vaccines, and vaccinations.
"""

from datetime import date
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from . import models, schemas
from .database import SessionLocal

# Dependency

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# User router
user_router = APIRouter()

@user_router.post("/", response_model=schemas.UserRead)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@user_router.get("/{user_id}", response_model=schemas.UserRead)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Vaccine router
vaccine_router = APIRouter()

@vaccine_router.post("/", response_model=schemas.VaccineRead)
def create_vaccine(vaccine: schemas.VaccineCreate, db: Session = Depends(get_db)):
    db_vaccine = models.Vaccine(**vaccine.dict())
    db.add(db_vaccine)
    db.commit()
    db.refresh(db_vaccine)
    return db_vaccine

@vaccine_router.get("/{vaccine_id}", response_model=schemas.VaccineRead)
def read_vaccine(vaccine_id: int, db: Session = Depends(get_db)):
    vaccine = db.query(models.Vaccine).filter(models.Vaccine.id == vaccine_id).first()
    if not vaccine:
        raise HTTPException(status_code=404, detail="Vaccine not found")
    return vaccine

# Vaccination router
vaccination_router = APIRouter()

@vaccination_router.post("/", response_model=schemas.VaccinationRead)
def create_vaccination(vaccination: schemas.VaccinationCreate, user_id: int, db: Session = Depends(get_db)):
    # Verify user exists
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    # Verify vaccine exists
    vaccine = db.query(models.Vaccine).filter(models.Vaccine.id == vaccination.vaccine_id).first()
    if not vaccine:
        raise HTTPException(status_code=404, detail="Vaccine not found")
    db_vaccination = models.Vaccination(user_id=user_id, vaccine_id=vaccination.vaccine_id, date=vaccination.date, side_effects=vaccination.side_effects or {})
    db.add(db_vaccination)
    db.commit()
    db.refresh(db_vaccination)
    return db_vaccination

@vaccination_router.get("/user/{user_id}", response_model=schemas.VaccinationList)
def list_vaccinations(user_id: int, db: Session = Depends(get_db)):
    vaccinations = db.query(models.Vaccination).filter(models.Vaccination.user_id == user_id).all()
    return schemas.VaccinationList(vaccinations=vaccinations)

# Core logic: next vaccination date calculation
@vaccination_router.get("/next/{user_id}")
def next_vaccination(user_id: int, db: Session = Depends(get_db)):
    # Simplified example: return the next vaccine that user hasn't received yet
    # In real scenario, use vaccine schedules and intervals
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    # Get all vaccines
    all_vaccines = db.query(models.Vaccine).all()
    # Get user's received vaccine ids
    received_ids = {v.vaccine_id for v in db.query(models.Vaccination).filter(models.Vaccination.user_id == user_id).all()}
    next_vaccine = next((v for v in all_vaccines if v.id not in received_ids), None)
    if not next_vaccine:
        return {"message": "All vaccines received"}
    return {"next_vaccine": next_vaccine.name}
