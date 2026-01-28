"""Seed the database with sample data."""

import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()


async def seed_database():
    client = AsyncIOMotorClient(os.getenv("MONGODB_URL", "mongodb://localhost:27017"))
    db = client[os.getenv("MONGODB_DB_NAME", "hospital_db")]
    
    # Clear existing data
    await db.doctors.delete_many({})
    await db.departments.delete_many({})
    await db.appointments.delete_many({})
    await db.patients.delete_many({})
    
    # Seed Departments
    departments = [
        {
            "department_id": "dept_001",
            "name": "Cardiology",
            "description": "Heart and cardiovascular system care",
            "location": "Building A, Floor 3",
            "phone": "+1-229-213-9501",
            "services": ["ECG", "Echocardiography", "Cardiac Stress Test", "Angiography"]
        },
        {
            "department_id": "dept_002",
            "name": "Neurology",
            "description": "Brain and nervous system disorders",
            "location": "Building B, Floor 2",
            "phone": "+1-229-213-9502",
            "services": ["EEG", "MRI", "Neurological Examination", "Stroke Care"]
        },
        {
            "department_id": "dept_003",
            "name": "Orthopedics",
            "description": "Bone, joint, and muscle care",
            "location": "Building A, Floor 1",
            "phone": "+1-229-213-9503",
            "services": ["X-Ray", "Fracture Treatment", "Joint Replacement", "Physical Therapy"]
        },
        {
            "department_id": "dept_004",
            "name": "Pediatrics",
            "description": "Children's health and development",
            "location": "Building C, Floor 1",
            "phone": "+1-229-213-9504",
            "services": ["Vaccinations", "Growth Monitoring", "Child Care", "Newborn Care"]
        },
        {
            "department_id": "dept_005",
            "name": "General Medicine",
            "description": "Primary care and general health",
            "location": "Building A, Floor 2",
            "phone": "+1-229-213-9505",
            "services": ["Health Checkups", "Fever Management", "Diabetes Care", "Hypertension"]
        },
    ]
    await db.departments.insert_many(departments)
    
    # Seed Doctors
    doctors = [
        {
            "doctor_id": "doc_001",
            "name": "Dr. Sarah Ahmed",
            "specialization": "Cardiologist",
            "department": "Cardiology",
            "phone": "+1-229-213-9601",
            "email": "sarah.ahmed@hospital.com",
            "working_hours": [
                {"day": "Monday", "start_time": "09:00", "end_time": "17:00", "is_available": True},
                {"day": "Tuesday", "start_time": "09:00", "end_time": "17:00", "is_available": True},
                {"day": "Wednesday", "start_time": "09:00", "end_time": "17:00", "is_available": True},
                {"day": "Thursday", "start_time": "09:00", "end_time": "17:00", "is_available": True},
                {"day": "Friday", "start_time": "09:00", "end_time": "13:00", "is_available": True},
                {"day": "Saturday", "start_time": "00:00", "end_time": "00:00", "is_available": False},
                {"day": "Sunday", "start_time": "00:00", "end_time": "00:00", "is_available": False},
            ],
            "consultation_duration": 30
        },
        {
            "doctor_id": "doc_002",
            "name": "Dr. Michael Chen",
            "specialization": "Neurologist",
            "department": "Neurology",
            "phone": "+1-229-213-9602",
            "email": "michael.chen@hospital.com",
            "working_hours": [
    {"day": "Monday", "start_time": "10:00", "end_time": "18:00", "is_available": True},
    {"day": "Tuesday", "start_time": "10:00", "end_time": "18:00", "is_available": True},
    {"day": "Wednesday", "start_time": "10:00", "end_time": "18:00", "is_available": True},
    {"day": "Thursday", "start_time": "10:00", "end_time": "18:00", "is_available": True},
    {"day": "Friday", "start_time": "10:00", "end_time": "14:00", "is_available": True},
    {"day": "Saturday", "start_time": "00:00", "end_time": "00:00", "is_available": False},
    {"day": "Sunday", "start_time": "00:00", "end_time": "00:00", "is_available": False},
    ],
    "consultation_duration": 45
    },
    {
    "doctor_id": "doc_003",
    "name": "Dr. Emily Rodriguez",
    "specialization": "Orthopedic Surgeon",
    "department": "Orthopedics",
    "phone": "+1-229-213-9603",
    "email": "emily.rodriguez@hospital.com",
    "working_hours": [
    {"day": "Monday", "start_time": "08:00", "end_time": "16:00", "is_available": True},
    {"day": "Tuesday", "start_time": "08:00", "end_time": "16:00", "is_available": True},
    {"day": "Wednesday", "start_time": "08:00", "end_time": "16:00", "is_available": True},
    {"day": "Thursday", "start_time": "08:00", "end_time": "16:00", "is_available": True},
    {"day": "Friday", "start_time": "08:00", "end_time": "12:00", "is_available": True},
    {"day": "Saturday", "start_time": "09:00", "end_time": "13:00", "is_available": True},
    {"day": "Sunday", "start_time": "00:00", "end_time": "00:00", "is_available": False},
    ],
    "consultation_duration": 30
    },
    {
    "doctor_id": "doc_004",
    "name": "Dr. James Wilson",
    "specialization": "Pediatrician",
    "department": "Pediatrics",
    "phone": "+1-229-213-9604",
    "email": "james.wilson@hospital.com",
    "working_hours": [
    {"day": "Monday", "start_time": "09:00", "end_time": "17:00", "is_available": True},
    {"day": "Tuesday", "start_time": "09:00", "end_time": "17:00", "is_available": True},
    {"day": "Wednesday", "start_time": "09:00", "end_time": "17:00", "is_available": True},
    {"day": "Thursday", "start_time": "09:00", "end_time": "17:00", "is_available": True},
    {"day": "Friday", "start_time": "09:00", "end_time": "17:00", "is_available": True},
    {"day": "Saturday", "start_time": "10:00", "end_time": "14:00", "is_available": True},
    {"day": "Sunday", "start_time": "00:00", "end_time": "00:00", "is_available": False},
    ],
    "consultation_duration": 20
    },
    {
    "doctor_id": "doc_005",
    "name": "Dr. Aisha Khan",
    "specialization": "General Physician",
    "department": "General Medicine",
    "phone": "+1-229-213-9605",
    "email": "aisha.khan@hospital.com",
    "working_hours": [
    {"day": "Monday", "start_time": "08:00", "end_time": "20:00", "is_available": True},
    {"day": "Tuesday", "start_time": "08:00", "end_time": "20:00", "is_available": True},
    {"day": "Wednesday", "start_time": "08:00", "end_time": "20:00", "is_available": True},
    {"day": "Thursday", "start_time": "08:00", "end_time": "20:00", "is_available": True},
    {"day": "Friday", "start_time": "08:00", "end_time": "20:00", "is_available": True},
    {"day": "Saturday", "start_time": "09:00", "end_time": "17:00", "is_available": True},
    {"day": "Sunday", "start_time": "10:00", "end_time": "14:00", "is_available": True},
    ],
    "consultation_duration": 15
    },
    ]
    await db.doctors.insert_many(doctors)
    print("Database seeded successfully.")
    await client.close()
if __name__ == "__main__":
    asyncio.run(seed_database())