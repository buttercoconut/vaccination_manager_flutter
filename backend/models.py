from sqlalchemy import Column, Integer, String, Date, ForeignKey, JSON
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    birth_date = Column(Date, nullable=False)
    phone = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    # 비밀번호는 해시 저장
    hashed_password = Column(String, nullable=False)
    vaccinations = relationship("Vaccination", back_populates="user")

class Vaccine(Base):
    __tablename__ = "vaccines"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    manufacturer = Column(String, nullable=False)
    efficacy = Column(String)
    interval_days = Column(Integer, nullable=False)  # 권장 접종 간격(일)
    vaccinations = relationship("Vaccination", back_populates="vaccine")

class Vaccination(Base):
    __tablename__ = "vaccinations"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    vaccine_id = Column(Integer, ForeignKey("vaccines.id"), nullable=False)
    date = Column(Date, nullable=False)
    side_effects = Column(JSON, default={})  # 예: {"fever": true, "pain": "moderate"}

    user = relationship("User", back_populates="vaccinations")
    vaccine = relationship("Vaccine", back_populates="vaccinations")
