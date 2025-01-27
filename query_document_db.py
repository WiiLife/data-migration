from pymongo import MongoClient
from datetime import datetime

# connect to mongodb
mongo_client = MongoClient('mongodb://localhost:27017/')

db = mongo_client["all_prescriptions_db"]
db_presc = db["prescriptions"]
db_rep_presc = db["repeatable prescriptions"]  

# delete the data in the two collections
# db_presc.delete_many({})
# db_rep_presc.delete_many({})

def display_query(collection, query):
    repr = ""
    for x in collection.find(query):
        repr += "\n"
        for key, value in x.items():
            repr += f"{key}: {value}\n"
    return repr

# find all prescriptions of Amoxicillin
# print(display_query(db_presc, {"prescription_name": "Amoxicillin"}))
# print(display_query(db_rep_presc, {"prescription_name": "Amoxicillin"}))


# find all the prescriptions taken by patient 1
# print(display_query(db_presc, {"patient": 1}))
# print(display_query(db_rep_presc, {"patient": 1}))

# find all prescriptions issed after the 20th dec 2024
print(display_query(db_presc, {"issue_date": {"$gt": datetime(2024, 12, 20)}}))    
print(display_query(db_rep_presc, {"issue_date": {"$gt": datetime(2024, 12, 20)}}))    
