from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session, declarative_base
import configparser
import os
import sqlalchemy
import random
from datetime import date
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
import time

from models import Repeatable_Prescription, Prescription, Specialization, InternalDoctor, ExternalDoctor, Diagnosis, Patient, Visit, Report

def create_connection():
    # Read configuration file
    config = configparser.ConfigParser()
    config_path = os.path.join(os.path.dirname(__file__), 'config.ini')
    config.read(config_path)

    # Get database credentials
    db_config = config['database']
    username = db_config['username']
    password = db_config['password']
    host = db_config['host']
    port = db_config['port']
    service_name = db_config['service_name']

    # Creating Oracle connection string
    connection_string = f"oracle+oracledb://{username}:{password}@{host}:{port}/{service_name}"
    engine = create_engine(connection_string)
    return engine

def add_prescription(issue_date, patient, quantity, prescription_name, direction_of_use, medication_strength, internal_doctor, dosage_form):
    
    if type(issue_date) != date:
        raise ValueError("insert date as a date object!")
    elif type(patient) != int:
        raise ValueError("insert patient id as int!")
    elif type(quantity) != int:
        raise ValueError("insert quantity as int!")
    elif type(prescription_name) != str:
        raise ValueError("insert prescrtiption name as string!")
    elif type(direction_of_use) != str:
        raise ValueError("insert directions of use as string!")
    elif medication_strength not in ["high", "medium", "low"]:
        raise ValueError("medication strength must be string: [high, medium, low]")
    elif type(internal_doctor) != int:
        raise ValueError("internal doctor must be int!")
    elif type(dosage_form) != str:
        raise ValueError("dosage form must be string!")

    engine = create_connection()
    with Session(engine) as session:

        try:
            prescription = Prescription(
                issue_date=issue_date,
                patient=patient,
                quantity=quantity,
                prescription_name=prescription_name,
                direction_of_use=direction_of_use,
                medication_strength=medication_strength,
                internal_doctor=internal_doctor,
                dosage_form=dosage_form,
            )
        except IntegrityError:
            session.rollback()
            raise RuntimeError("prescription already added")

        session.add(prescription)
        session.commit()

    print(f"prescription {prescription_name} added!")

def add_repeatable_prescription(issue_date, patient, quantity, times_presc_can_be_used, interval_day_period_between_presc, prescription_name, direction_of_use, medication_strength, internal_doctor, dosage_form):
    
    if type(issue_date) != date:
        raise ValueError("insert date as a date object!")
    elif type(patient) != int:
        raise ValueError("insert patient id as int!")
    elif type(quantity) != int:
        raise ValueError("insert quantity as int!")
    elif type(prescription_name) != str:
        raise ValueError("insert prescrtiption name as string!")
    elif type(direction_of_use) != str:
        raise ValueError("insert directions of use as string!")
    elif medication_strength not in ["high", "medium", "low"]:
        raise ValueError("medication strength must be string: [high, medium, low]")
    elif type(internal_doctor) != int:
        raise ValueError("internal doctor must be int!")
    elif type(dosage_form) != str:
        raise ValueError("dosage form must be string!")
    elif type(times_presc_can_be_used) != int:
        raise ValueError("times presc can be used must be an int!")
    elif type(interval_day_period_between_presc) != int:
        raise ValueError("interval day period between presc must be an int!")

    engine = create_connection()
    with Session(engine) as session:

        try:
            prescription = Repeatable_Prescription(
                issue_date=issue_date,
                patient=patient,
                quantity=quantity,
                times_presc_can_be_used=times_presc_can_be_used,
                interval_day_period_between_presc=interval_day_period_between_presc,
                prescription_name=prescription_name,
                direction_of_use=direction_of_use,
                medication_strength=medication_strength,
                internal_doctor=internal_doctor,
                dosage_form=dosage_form,
            )

        except IntegrityError:
            session.rollback()
            raise RuntimeError("prescription already added")

        session.add(prescription)
        session.commit()

    print(f"repeatable prescription {prescription_name} added!")



# 4x repeatbale prescriptions
add_repeatable_prescription(
    issue_date=date(2024, 12, 19),
    patient=1,
    quantity=30,
    times_presc_can_be_used=3,
    interval_day_period_between_presc=7,
    prescription_name="Ibuprofen",
    direction_of_use="Take one tablet every 8 hours",
    medication_strength="medium",
    internal_doctor=1,
    dosage_form="Tablet",
    )


add_repeatable_prescription(
    issue_date=date(2024, 12, 20),
    patient=2,
    quantity=40,
    times_presc_can_be_used=5,
    interval_day_period_between_presc=10,
    prescription_name="Amoxicillin",
    direction_of_use="Take one capsule every 8 hours with meals",
    medication_strength="high",
    internal_doctor=2,
    dosage_form="Capsule",
)

add_repeatable_prescription(
    issue_date=date(2024, 12, 21),
    patient=3,
    quantity=20,
    times_presc_can_be_used=4,
    interval_day_period_between_presc=15,
    prescription_name="Paracetamol",
    direction_of_use="Take one tablet every 6 hours",
    medication_strength="low",
    internal_doctor=3,
    dosage_form="Tablet",
)

add_repeatable_prescription(
    issue_date=date(2024, 12, 22),
    patient=4,
    quantity=25,
    times_presc_can_be_used=2,
    interval_day_period_between_presc=14,
    prescription_name="Cetirizine",
    direction_of_use="Take one tablet before bed",
    medication_strength="medium",
    internal_doctor=4,
    dosage_form="Tablet",
)

# 6x normal prescriptions
add_prescription(
    issue_date=date(2024, 12, 19), 
    patient=1, 
    quantity=30, 
    prescription_name="Paracetamol",
    direction_of_use="Take one tablet every 6 hours",
    medication_strength="low",
    internal_doctor=2,
    dosage_form="Capsule",
    )


add_prescription(
    issue_date=date(2024, 12, 20),
    patient=1,
    quantity=15,
    prescription_name="Ibuprofen",
    direction_of_use="Take one tablet every 8 hours",
    medication_strength="medium",
    internal_doctor=3,
    dosage_form="Tablet",
)

add_prescription(
    issue_date=date(2024, 12, 21),
    patient=4,
    quantity=25,
    prescription_name="Ciprofloxacin",
    direction_of_use="Take one capsule every 12 hours",
    medication_strength="low",
    internal_doctor=4,
    dosage_form="Capsule",
)

add_prescription(
    issue_date=date(2024, 12, 22),
    patient=1,
    quantity=10,
    prescription_name="Cetirizine",
    direction_of_use="Take one tablet before bed",
    medication_strength="medium",
    internal_doctor=5,
    dosage_form="Tablet",
)

add_prescription(
    issue_date=date(2024, 12, 23),
    patient=6,
    quantity=30,
    prescription_name="Amoxicillin",
    direction_of_use="Take one capsule every 8 hours with meals",
    medication_strength="high",
    internal_doctor=1,
    dosage_form="Capsule",
)

add_prescription(
    issue_date=date(2024, 12, 24),
    patient=7,
    quantity=18,
    prescription_name="Loratadine",
    direction_of_use="Take one tablet in the morning",
    medication_strength="low",
    internal_doctor=2,
    dosage_form="Tablet",
)
