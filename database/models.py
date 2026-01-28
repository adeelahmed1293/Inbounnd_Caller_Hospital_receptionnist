"""Data models for MongoDB documents."""

from typing import List, Optional
from datetime import datetime, time
from pydantic import BaseModel, Field


class WorkingHours(BaseModel):
    """Working hours for a specific day."""
    day: str  # Monday, Tuesday, etc.
    start_time: str  # "09:00"
    end_time: str  # "17:00"
    is_available: bool = True


class Doctor(BaseModel):
    """Doctor model."""
    doctor_id: str
    name: str
    specialization: str
    department: str
    phone: Optional[str] = None
    email: Optional[str] = None
    working_hours: List[WorkingHours]
    consultation_duration: int = 30  # minutes


class Department(BaseModel):
    """Department model."""
    department_id: str
    name: str
    description: str
    location: str  # e.g., "Building A, Floor 2"
    phone: str
    services: List[str]


class Patient(BaseModel):
    """Patient model."""
    patient_id: Optional[str] = None
    name: str
    phone: str
    email: Optional[str] = None
    date_of_birth: Optional[str] = None
    address: Optional[str] = None
    medical_history: Optional[List[str]] = None


class Appointment(BaseModel):
    """Appointment model."""
    appointment_id: Optional[str] = None
    patient_id: str
    patient_name: str
    patient_phone: str
    doctor_id: str
    doctor_name: str
    department: str
    date: str  # "2026-01-28"
    time: str  # "14:30"
    reason: str
    status: str = "scheduled"  # scheduled, completed, cancelled
    created_at: str = Field(default_factory=lambda: datetime.now().isoformat())