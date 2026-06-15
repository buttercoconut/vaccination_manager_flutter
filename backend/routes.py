"""FastAPI router with CRUD endpoints."""

from datetime import date
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from . import models, schemas
from .database import get_db

router = APIRouter(prefix="/api", tags=["vaccination_manager"])

# User endpoints
@router.post("/users", response_model=schemas.UserOut, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = models.User(name=user.name, birth_date=user.birth_date, phone=user.phone, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/users/{user_id}", response_model=schemas.UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Vaccine endpoints
@router.post("/vaccines", response_model=schemas.VaccineOut, status_code=status.HTTP_201_CREATED)
def create_vaccine(vaccine: schemas.VaccineCreate, db: Session = Depends(get_db)):
    db_vaccine = models.Vaccine(name=vaccine.name, manufacturer=vaccine.manufacturer, efficacy=vaccine.efficacy)
    db.add(db_vaccine)
    db.commit()
    db.refresh(db_vaccine)
    return db_vaccine

@router.get("/vaccines", response_model=List[schemas.VaccineOut])
def list_vaccines(db: Session = Depends(get_db)):
    return db.query(models.Vaccine).all()

# Vaccination endpoints
@router.post("/users/{user_id}/vaccinations", response_model=schemas.VaccinationOut, status_code=status.HTTP_201_CREATED)
def add_vaccination(user_id: int, vaccination: schemas.VaccinationCreate, db: Session = Depends(get_db)):
    # Validate user exists
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    # Validate vaccine exists
    vaccine = db.query(models.Vaccine).filter(models.Vaccine.id == vaccination.vaccine_id).first()
    if not vaccine:
        raise HTTPException(status_code=404, detail="Vaccine not found")
    db_vaccination = models.Vaccination(user_id=user_id, vaccine_id=vaccination.vaccine_id, date=vaccination.date, side_effects=vaccination.side_effects)
    db.add(db_vaccination)
    db.commit()
    db.refresh(db_vaccination)
    return db_vaccination

@router.get("/users/{user_id}/vaccinations", response_model=List[schemas.VaccinationOut])
def list_vaccinations(user_id: int, db: Session = Depends(get_db)):
    return db.query(models.Vaccination).filter(models.Vaccination.user_id == user_id).all()

# Core logic: next vaccination date calculation
@router.get("/users/{user_id}/next-vaccination", response_model=dict)
def next_vaccination(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    # Simplified example: assume each vaccine requires 1 year interval
    last_vacc = db.query(models.Vaccination).filter(models.Vaccination.user_id == user_id).order_by(models.Vaccination.date.desc()).first()
    if not last_vacc:
        return {"next_date": None, "message": "No vaccination history"}
    next_date = last_vacc.date.replace(year=last_vacc.date.year + 1)
    return {"next_date": next_date, "message": "Next due date calculated"}
