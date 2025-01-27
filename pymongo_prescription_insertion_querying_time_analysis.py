from pymongo import MongoClient
from datetime import datetime, timedelta
import time
import matplotlib.pyplot as plt
import numpy as np
import random

mongo_client = MongoClient('mongodb://localhost:27017/')
db = mongo_client["all_prescriptions_db"]  
db_presc = db["prescriptions"] 

def generate_prescriptions(n):
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
            prescription = {
                "issue_date": datetime(2024, 12, 19) + timedelta(days=random.randint(0, 30)),
                "patient": random.randint(1, 20),
                "quantity": random.randint(5, 60),
                "prescription_name": random.choice(prescription_names),
                "direction_of_use": random.choice(directions),
                "medication_strength": random.choice(strengths),
                "internal_doctor": random.randint(1, 10),
                "dosage_form": random.choice(dosage_forms),
            }
            prescriptions.append(prescription)
        else:
            rep_prescription = {
                "issue_date": datetime(2024, 12, 19) + timedelta(days=random.randint(0, 30)),
                "patient": random.randint(1, 20),
                "quantity": random.randint(5, 60),
                "times_presc_can_be_used": random.randint(1, 50),
                "interval_day_period_between_presc": random.randint(1, 10),
                "prescription_name": random.choice(prescription_names),
                "direction_of_use": random.choice(directions),
                "medication_strength": random.choice(strengths),
                "internal_doctor": random.randint(1, 10),
                "dosage_form": random.choice(dosage_forms),
            }
            prescriptions.append(rep_prescription)

    return prescriptions

times = []
times_1 = []
for _ in range(100):
    # data insertion
    n_prescriptions = generate_prescriptions(1000)

    time_0 = time.perf_counter()
    db_presc.insert_many(n_prescriptions)
    time_1 = time.perf_counter()

    times.append(time_1 - time_0)   

    # data querying
    time_2 = time.perf_counter()
    db_presc.find()
    time_3 = time.perf_counter()

    times_1.append(time_3 - time_2)

    db_presc.delete_many({})

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


