"""API routes for vaccination manager.

Includes CRUD for users, vaccines, and vaccinations.
"""

from datetime import date, timedelta
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from . import models, schemas
from .database import get_db

router = APIRouter()

# ---------- User endpoints ----------
@router.post("/users", response_model=schemas.UserRead, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/users/{user_id}", response_model=schemas.UserRead)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# ---------- Vaccine endpoints ----------
@router.post("/vaccines", response_model=schemas.VaccineRead, status_code=status.HTTP_201_CREATED)
def create_vaccine(vaccine: schemas.VaccineCreate, db: Session = Depends(get_db)):
    db_vaccine = models.Vaccine(**vaccine.dict())
    db.add(db_vaccine)
    db.commit()
    db.refresh(db_vaccine)
    return db_vaccine

@router.get("/vaccines", response_model=List[schemas.VaccineRead])
def list_vaccines(db: Session = Depends(get_db)):
    return db.query(models.Vaccine).all()

# ---------- Vaccination endpoints ----------
@router.post("/users/{user_id}/vaccinations", response_model=schemas.VaccinationRead, status_code=status.HTTP_201_CREATED)
def create_vaccination(user_id: int, vaccination: schemas.VaccinationCreate, db: Session = Depends(get_db)):
    # Validate user exists
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    # Validate vaccine exists
    vaccine = db.query(models.Vaccine).filter(models.Vaccine.id == vaccination.vaccine_id).first()
    if not vaccine:
        raise HTTPException(status_code=404, detail="Vaccine not found")
    db_vaccination = models.Vaccination(user_id=user_id, **vaccination.dict())
    db.add(db_vaccination)
    db.commit()
    db.refresh(db_vaccination)
    return db_vaccination

@router.get("/users/{user_id}/vaccinations", response_model=List[schemas.VaccinationRead])
def list_vaccinations(user_id: int, db: Session = Depends(get_db)):
    return db.query(models.Vaccination).filter(models.Vaccination.user_id == user_id).all()

# ---------- Core logic: next vaccination due ----------
@router.get("/users/{user_id}/next_due", response_model=dict)
def next_due(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    # Find latest vaccination per vaccine
    latest = (
        db.query(models.Vaccination)
        .filter(models.Vaccination.user_id == user_id)
        .order_by(models.Vaccination.date.desc())
        .first()
    )
    if not latest:
        return {"message": "No vaccination records. Please add one."}
    vaccine = db.query(models.Vaccine).filter(models.Vaccine.id == latest.vaccine_id).first()
    next_date = latest.date + timedelta(days=vaccine.interval_days)
    return {"next_due_date": next_date.isoformat(), "vaccine": vaccine.name}
