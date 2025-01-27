from sqlalchemy.orm import Session
from models import Repeatable_Prescription, Prescription, Specialization, InternalDoctor, ExternalDoctor, Diagnosis, Patient, Visit, Report

# test queries
def get_first_prescription(session):
    prescription = session.query(Prescription).first()
    print("First Prescription:\n")
    print(
        f"Issue Date: {prescription.issue_date},\nPatient: {prescription.patient},\n"
        f"Quantity: {prescription.quantity},\nPrescription Name: {prescription.prescription_name},\n"
        f"Direction of Use: {prescription.direction_of_use},\nStrength: {prescription.medication_strength},\n"
        f"Doctor: {prescription.internal_doctor},\nDosage Form: {prescription.dosage_form}\n"
    )


def get_prescription_and_doc(session):
    results = session.query(Prescription, InternalDoctor).join(InternalDoctor, Prescription.internal_doctor == InternalDoctor.id).all()
    for presc, doctor in results:
        print(f"Prescription: {presc.prescription_name}, Doctor: {doctor.name}")


def get_davids_prescriptions_in_tablet_form(session):
    results = session.query(
        Prescription,
        InternalDoctor,
        Patient
    ).join(
        Patient, Prescription.patient == Patient.id
    ).join(
        InternalDoctor, Prescription.internal_doctor == InternalDoctor.id
    ).filter(and_(Patient.name=="david", Prescription.dosage_form=="Tablet")).all()

    for presc, doctor, patient in results:
        print(f"{presc.prescription_name} was given by {doctor.surname} to {patient.name}")


def prescription_dosage_forms(session):
    tablet_prescriptions = session.query(Prescription).filter(Prescription.dosage_form=="Tablet")
    capsule_prescriptions = session.query(Prescription).filter(Prescription.dosage_form=="Capsule")
    print("Tablet prescriptions:")
    for presc in tablet_prescriptions:
        print(presc.prescription_name)
    print()
    print("Capsule prescriptions:")
    for presc in capsule_prescriptions: 
        print(presc.prescription_name) 


def patient_with_more_than_2_prescriptions(session):
    results = (
        session.query(
            Patient.id, 
            Patient.name, 
            func.count(Prescription.prescription_name).label("prescription_count")
        )
        .join(Prescription, Prescription.patient == Patient.id)
        .group_by(Patient.id, Patient.name)
        .having(func.count(Prescription.prescription_name) > 2)
        .all()
    )

    for patient_id, name, prescription_count in results:
        print(f"Patient ID: {patient_id}, Name: {name}, Prescriptions: {prescription_count}")