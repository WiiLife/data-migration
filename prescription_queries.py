from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, select, text, and_, or_
import configparser
import os

from models import Repeatable_Prescription, Prescription, Specialization, InternalDoctor, ExternalDoctor, Diagnosis, Patient, Visit, Report
from test_queries_alchemy import patient_with_more_than_2_prescriptions, prescription_dosage_forms, get_davids_prescriptions_in_tablet_form, get_prescription_and_doc, get_first_prescription

# Connection configuration
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


engine = create_connection()
with Session(engine) as session:
    
    # test queries
    # patient_with_more_than_2_prescriptions(session)
    # prescription_dosage_forms(session) 
    # get_davids_prescriptions_in_tablet_form(session)
    # get_prescription_and_doc(session)
    get_first_prescription(session)

    """
    # find all prescriptions
    results = session.query(Prescription).all()
    for prescription in results:
        print(
        f"Issue Date: {prescription.issue_date},\nPatient: {prescription.patient},\n"
        f"Quantity: {prescription.quantity},\nPrescription Name: {prescription.prescription_name},\n"
        f"Direction of Use: {prescription.direction_of_use},\nStrength: {prescription.medication_strength},\n"
        f"Doctor: {prescription.internal_doctor},\nDosage Form: {prescription.dosage_form}\n"
    )
    """