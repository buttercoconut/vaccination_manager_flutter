"""
FastAPI router with CRUD endpoints.
"""

from datetime import date
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from . import models, schemas
from .database import get_db

router = APIRouter()

# User endpoints
@router.post("/users", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
def create_user(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = models.User(**user_in.dict(exclude={"password"}))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/users/{user_id}", response_model=schemas.User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Vaccine endpoints
@router.post("/vaccines", response_model=schemas.Vaccine, status_code=status.HTTP_201_CREATED)
def create_vaccine(vaccine_in: schemas.VaccineCreate, db: Session = Depends(get_db)):
    vaccine = models.Vaccine(**vaccine_in.dict())
    db.add(vaccine)
    db.commit()
    db.refresh(vaccine)
    return vaccine

@router.get("/vaccines", response_model=List[schemas.Vaccine])
def list_vaccines(db: Session = Depends(get_db)):
    return db.query(models.Vaccine).all()

# SideEffect endpoints
@router.post("/side_effects", response_model=schemas.SideEffect, status_code=status.HTTP_201_CREATED)
def create_side_effect(se_in: schemas.SideEffectCreate, db: Session = Depends(get_db)):
    se = models.SideEffect(**se_in.dict())
    db.add(se)
    db.commit()
    db.refresh(se)
    return se

# Vaccination endpoints
@router.post("/users/{user_id}/vaccinations", response_model=schemas.Vaccination, status_code=status.HTTP_201_CREATED)
def create_vaccination(user_id: int, vacc_in: schemas.VaccinationCreate, db: Session = Depends(get_db)):
    # Validate vaccine exists
    vaccine = db.query(models.Vaccine).filter(models.Vaccine.id == vacc_in.vaccine_id).first()
    if not vaccine:
        raise HTTPException(status_code=404, detail="Vaccine not found")
    # Validate user exists
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    vacc = models.Vaccination(user_id=user_id, vaccine_id=vacc_in.vaccine_id, date=vacc_in.date)
    # Attach side effects
    if vacc_in.side_effect_ids:
        side_effects = db.query(models.SideEffect).filter(models.SideEffect.id.in_(vacc_in.side_effect_ids)).all()
        vacc.side_effects.extend(side_effects)
    db.add(vacc)
    db.commit()
    db.refresh(vacc)
    return vacc

@router.get("/users/{user_id}/vaccinations", response_model=List[schemas.Vaccination])
def list_vaccinations(user_id: int, db: Session = Depends(get_db)):
    return db.query(models.Vaccination).filter(models.Vaccination.user_id == user_id).all()

# Core logic: next vaccination date calculation
@router.get("/users/{user_id}/next_vaccination", response_model=dict)
def next_vaccination(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    # Simplified example: assume each vaccine requires 1 year interval
    today = date.today()
    last_vacc = db.query(models.Vaccination).filter(models.Vaccination.user_id == user_id).order_by(models.Vaccination.date.desc()).first()
    if not last_vacc:
        return {"next_date": None, "message": "No vaccination history"}
    next_date = last_vacc.date.replace(year=last_vacc.date.year + 1)
    return {"next_date": next_date.isoformat()}
