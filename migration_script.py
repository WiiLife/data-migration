from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, select, text, and_, or_
import configparser
import os
from datetime import date, datetime

from pymongo import MongoClient

from models import Repeatable_Prescription, Prescription, Specialization, InternalDoctor, ExternalDoctor, Diagnosis, Patient, Visit, Report

# Connection configuration
def create_connection_sql():
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



engine = create_connection_sql()
with Session(engine) as session:

    # connection with pymongo
    mongo_client = MongoClient('mongodb://localhost:27017/')
    db = mongo_client["all_prescriptions_db"]   # database
    db_presc = db["prescriptions"]   # prescription collection
    db_rep_presc = db["repeatable prescriptions"]    # repeatable prescription table
    # print(mongo_client.list_database_names())


    prescription_table = session.query(Prescription).all()
    for row in prescription_table:
        if row:
            row_data = {column.name: getattr(row, column.name) for column in Prescription.__table__.columns}

            # mongodb doesn't accept date objects only datetime ones
            for key, value in row_data.items():
                if type(value) == date:
                    row_data[key] = datetime.combine(value, datetime.min.time())

            # check if prescription already added
            if db_presc.find_one({"issue_date": row_data["issue_date"], "prescription_name": row_data["prescription_name"]}):     # identifiable clause
                rep_issue_date = row_data["issue_date"]
                rep_prescription_name = row_data["prescription_name"]
                print(f"on {rep_issue_date}, {rep_prescription_name} already inserted!")
                continue    # if we found the same prescription we skip it
            else:
                db_presc.insert_one(row_data)

        else:
            raise ValueError("No records found in the Prescription table")

    print("prescription data converted!")

    rep_prescription_table = session.query(Repeatable_Prescription).all()
    for row in rep_prescription_table:
        if row:
            row_data = {column.name: getattr(row, column.name) for column in Repeatable_Prescription.__table__.columns}

            for key, value in row_data.items():
                if type(value) == date:
                    row_data[key] = datetime.combine(value, datetime.min.time())

            # check if repeated prescription already added
            if db_rep_presc.find_one({"issue_date": row_data["issue_date"], "prescription_name": row_data["prescription_name"]}):     # identifiable clause
                rep_issue_date = row_data["issue_date"]
                rep_prescription_name = row_data["prescription_name"]
                print(f"on {rep_issue_date}, {rep_prescription_name} already inserted!")
                continue    # if we found the same prescription we skip it
            else:
                db_rep_presc.insert_one(row_data)

        else:
            raise ValueError("No records found in the Prescription table")

    print("repeatable prescription data converted!")

"""
# visluaize the converted data
def display_mong_col(collection):
    repr = ""
    for x in collection.find():
        repr += "\n"
        for key, value in x.items():
            repr += f"{key}: {value}\n"
    return repr

print(display_mong_col(db_presc))
"""
