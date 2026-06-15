from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import date

from . import models, schemas
from .database import get_db

router = APIRouter()

# 유틸리티: 다음 접종일 계산

def calculate_next_due(user_birth: date, vaccine_interval: int) -> date:
    # 간단히 현재 날짜 기준으로 계산
    today = date.today()
    return today

# 사용자 CRUD 예시 (간단화)
@router.post("/users", response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = models.User(**user.dict(exclude={"password"}))
    # 비밀번호 해시 처리 생략
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# 백신 CRUD 예시
@router.post("/vaccines", response_model=schemas.VaccineOut)
def create_vaccine(vaccine: schemas.VaccineCreate, db: Session = Depends(get_db)):
    db_vaccine = models.Vaccine(**vaccine.dict())
    db.add(db_vaccine)
    db.commit()
    db.refresh(db_vaccine)
    return db_vaccine

# 예방접종 등록
@router.post("/", response_model=schemas.VaccinationOut)
def create_vaccination(vaccination: schemas.VaccinationCreate, db: Session = Depends(get_db)):
    db_vaccination = models.Vaccination(**vaccination.dict())
    db.add(db_vaccination)
    db.commit()
    db.refresh(db_vaccination)
    return db_vaccination

# 예방접종 목록 조회
@router.get("/", response_model=List[schemas.VaccinationOut])
def read_vaccinations(user_id: int, db: Session = Depends(get_db)):
    return db.query(models.Vaccination).filter(models.Vaccination.user_id == user_id).all()
