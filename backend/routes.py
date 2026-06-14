# routes.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import date
from typing import List

from . import models, schemas, database, auth

router = APIRouter()

# User routes
@router.post("/users", response_model=schemas.UserOut)
def create_user(user_in: schemas.UserCreate, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == user_in.email).first()
    if user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = auth.get_password_hash(user_in.password)
    user = models.User(
        name=user_in.name,
        birth_date=user_in.birth_date,
        phone=user_in.phone,
        email=user_in.email,
        hashed_password=hashed_password,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.get("/users/me", response_model=schemas.UserOut)
def read_users_me(current_user: models.User = Depends(auth.get_current_user)):
    return current_user

# Token route
@router.post("/token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(data={"sub": str(user.id)}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

# Vaccine routes
@router.post("/vaccines", response_model=schemas.VaccineOut)
def create_vaccine(vaccine_in: schemas.VaccineCreate, db: Session = Depends(database.get_db)):
    vaccine = models.Vaccine(**vaccine_in.dict())
    db.add(vaccine)
    db.commit()
    db.refresh(vaccine)
    return vaccine

@router.get("/vaccines", response_model=List[schemas.VaccineOut])
def list_vaccines(db: Session = Depends(database.get_db)):
    return db.query(models.Vaccine).all()

# Vaccination routes
@router.post("/vaccinations", response_model=schemas.VaccinationOut)
def create_vaccination(vaccination_in: schemas.VaccinationCreate, db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    vaccination = models.Vaccination(
        user_id=current_user.id,
        vaccine_id=vaccination_in.vaccine_id,
        date=vaccination_in.date,
        side_effects=vaccination_in.side_effects or {},
    )
    db.add(vaccination)
    db.commit()
    db.refresh(vaccination)
    return vaccination

@router.get("/vaccinations", response_model=List[schemas.VaccinationOut])
def list_vaccinations(db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    return db.query(models.Vaccination).filter(models.Vaccination.user_id == current_user.id).all()

# Core logic: next vaccination due date
@router.get("/vaccinations/next", response_model=schemas.VaccinationOut)
def next_vaccination_due(db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    # Find the most recent vaccination for each vaccine type
    latest = db.query(models.Vaccination).filter(models.Vaccination.user_id == current_user.id).order_by(models.Vaccination.date.desc()).first()
    if not latest:
        raise HTTPException(status_code=404, detail="No vaccination records found")
    vaccine = db.query(models.Vaccine).filter(models.Vaccine.id == latest.vaccine_id).first()
    next_date = latest.date + timedelta(days=vaccine.interval_days)
    return schemas.VaccinationOut(
        id=latest.id,
        user_id=latest.user_id,
        vaccine_id=latest.vaccine_id,
        date=next_date,
        side_effects={}
    )
