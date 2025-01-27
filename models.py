# models.py
from typing import List, Optional
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, Date, Integer


class Base(DeclarativeBase):
    pass


class Specialization(Base):
    __tablename__ = 'specialization'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))


class DoctorMixin:
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    surname: Mapped[str] = mapped_column(String(50))
    specialization: Mapped[int] = mapped_column(ForeignKey("specialization.id"))


class InternalDoctor(DoctorMixin, Base):
    __tablename__ = 'internal_doctor'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    surname: Mapped[str] = mapped_column(String(50))
    specialization: Mapped[int] = mapped_column(ForeignKey("specialization.id"))


class ExternalDoctor(DoctorMixin, Base):
    __tablename__ = 'external_doctor'
    street: Mapped[str] = mapped_column(String(50))
    postcode: Mapped[str] = mapped_column(String(50))
    city: Mapped[str] = mapped_column(String(50))
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    surname: Mapped[str] = mapped_column(String(50))
    specialization: Mapped[int] = mapped_column(ForeignKey("specialization.id"))


class Diagnosis(Base):
    __tablename__ = 'diagnosis'
    code: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(String(100))
    specialization: Mapped[int] = mapped_column(ForeignKey("specialization.id"))


class Patient(Base):
    __tablename__ = 'patient'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    surname: Mapped[str] = mapped_column(String(50))
    birthdate: Mapped[Date] = mapped_column(Date)
    street: Mapped[str] = mapped_column(String(50))
    postcode: Mapped[str] = mapped_column(String(50))
    city: Mapped[str] = mapped_column(String(50))


class Visit(Base):
    __tablename__ = 'visit'
    v_number: Mapped[int] = mapped_column(primary_key=True)
    v_date: Mapped[Date] = mapped_column(Date)
    internal_doctor_id: Mapped[int] = mapped_column(ForeignKey("internal_doctor.id"))
    external_doctor_id: Mapped[int] = mapped_column(ForeignKey("internal_doctor.id"))
    


class Report(Base):
    __tablename__ = 'report'
    v_number: Mapped[int] = mapped_column(ForeignKey("visit.v_number"), primary_key=True)
    diagnosis: Mapped[int] = mapped_column(ForeignKey("diagnosis.code"), primary_key=True)

# Assignment .1 - Relational schema definition

class Repeatable_Prescription(Base):
    __tablename__ = "repeatable_prescription"
    issue_date: Mapped[Date] = mapped_column(Date, primary_key=True)
    patient: Mapped[int] = mapped_column(ForeignKey("patient.id"))
    quantity: Mapped[int] = mapped_column(Integer)
    times_presc_can_be_used: Mapped[int] = mapped_column(Integer)
    interval_day_period_between_presc: Mapped[int] = mapped_column(Integer)
    direction_of_use: Mapped[str] = mapped_column(String(500))
    medication_strength: Mapped[str] = mapped_column(String(10))
    prescription_name: Mapped[str] = mapped_column(String(50), primary_key=True)
    internal_doctor: Mapped[int] = mapped_column(ForeignKey("internal_doctor.id"))
    dosage_form: Mapped[str] = mapped_column(String(50))
    

class Prescription(Base):
    __tablename__ = "prescription"
    issue_date: Mapped[Date] = mapped_column(Date, primary_key=True)
    patient: Mapped[int] = mapped_column(ForeignKey("patient.id"))
    quantity: Mapped[int] = mapped_column(Integer)
    direction_of_use: Mapped[str] = mapped_column(String(500))
    medication_strength: Mapped[str] = mapped_column(String(10))
    prescription_name: Mapped[str] = mapped_column(String(50), primary_key=True)
    internal_doctor: Mapped[int] = mapped_column(ForeignKey("internal_doctor.id"))
    dosage_form: Mapped[str] = mapped_column(String(50))
