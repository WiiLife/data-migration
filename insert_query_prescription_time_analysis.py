from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session, declarative_base
import configparser
import os
import sqlalchemy
import random
from datetime import date, datetime, timedelta
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
import time

from models import Repeatable_Prescription, Prescription, Specialization, InternalDoctor, ExternalDoctor, Diagnosis, Patient, Visit, Report

# ! note--> to run the script you must fisrt have the tables created with all their data in oracle db

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

def generate_prescriptions(n, session):
    prescription_names = [
        "Paracetamol", "Ibuprofen", "Ciprofloxacin", "Cetirizine", "Amoxicillin", "Loratadine",
        "Metformin", "Atorvastatin", "Omeprazole", "Hydrochlorothiazide"
    ]
    directions = [
        "Take one tablet every 6 hours",
        "Take one tablet every 8 hours",
        "Take one capsule every 12 hours",
        "Take one tablet before bed",
        "Take one capsule every 8 hours with meals",
        "Take one tablet in the morning",
        "Take one tablet twice daily",
        "Take one capsule every 24 hours"
    ]
    strengths = ["low", "medium", "high"]
    dosage_forms = ["Tablet", "Capsule", "Syrup", "Injection"]

    prescriptions = []
    for i in range(n):
        if i % 2 == 0:
            try:
                prescription = Prescription(
                    issue_date = date(2024, 12, 19) + timedelta(days=random.randint(0, 30)),
                    patient = random.randint(1, 9),
                    quantity = random.randint(5, 60),
                    prescription_name = random.choice(prescription_names),
                    direction_of_use = random.choice(directions),
                    medication_strength = random.choice(strengths),
                    internal_doctor = random.randint(1, 10),
                    dosage_form = random.choice(dosage_forms),
                )
                prescriptions.append(prescription)
            except IntegrityError:
                session.rollback()
                raise RuntimeError("prescription already added")
        else:
            try:
                rep_prescription = Repeatable_Prescription(
                    issue_date = date(2024, 12, 19) + timedelta(days=random.randint(0, 30)),
                    patient = random.randint(1, 9),
                    quantity = random.randint(5, 60),
                    times_presc_can_be_used = random.randint(1, 50),
                    interval_day_period_between_presc = random.randint(1, 10),
                    prescription_name = random.choice(prescription_names),
                    direction_of_use = random.choice(directions),
                    medication_strength = random.choice(strengths),
                    internal_doctor = random.randint(1, 10),
                    dosage_form = random.choice(dosage_forms),
                )
                prescriptions.append(rep_prescription)
            except IntegrityError:
                session.rollback()
                raise RuntimeError("prescription already added")

    return prescriptions


engine = create_connection()
with Session(engine) as session:

    times = []
    times_1 = []
    for _ in range(100):

        # if randomly there are two prescriptions with the same primary keys we need to skip that prescription
        n_prescriptions = generate_prescriptions(2000, session)
        new_n_prescriptions = []
        unique_primary_keys = []
        i = 0
        for presc in n_prescriptions:
            if i == 1001:
                break
            elif (presc.issue_date, presc.prescription_name) in unique_primary_keys:
                continue
            else:
                unique_primary_keys.append((presc.issue_date, presc.prescription_name))
                i += 1
        
        # data insertion

        # adding the unique primary key prescriptions
        time_0 = time.perf_counter()
        session.add_all(new_n_prescriptions)
        time_1 = time.perf_counter()
        session.commit()

        times.append(time_1-time_0)

        # data querying
        time_2 = time.perf_counter()
        session.query(Repeatable_Prescription).all()
        session.query(Prescription).all()
        time_3 = time.perf_counter()

        times_1.append(time_3 - time_2)

        # delete the prescriptions
        session.execute(text("DELETE FROM prescription")) 
        session.execute(text("DELETE FROM repeatable_prescription"))
        session.commit()
        
        print(f"time taken insertion: {time_1-time_0:.10f}s")
        print(f"time taken query: {time_3-time_2:.10f}s")

import matplotlib.pyplot as plt
import numpy as np

fig, axs = plt.subplots(2, 1)

axs[0].plot(range(100), times)
axs[0].plot((0, 100), (np.mean(times), np.mean(times)))
axs[0].set_title("inserting 1000 prescriptions")
axs[0].set_ylabel("time (s)")
axs[0].set_xlabel("iteration")

axs[1].plot(range(100), times_1)
axs[1].plot((0, 100), (np.mean(times_1), np.mean(times_1)))
axs[1].set_title("querying 1000 prescriptions")
axs[1].set_ylabel("time (s)")
axs[1].set_xlabel("iteration")

plt.tight_layout()
plt.show()

print(f"mean insertion time: {np.mean(times)}")
print(f"mean query time: {np.mean(times_1)}")

