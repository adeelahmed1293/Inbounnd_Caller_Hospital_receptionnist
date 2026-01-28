"""Tools package."""

from .weather import get_weather
from .datetime_tool import get_current_datetime, get_current_date, get_current_time
from .doctor_schedule import get_doctor_schedule, check_doctor_availability, list_all_departments
from .appointment import book_appointment, check_patient_appointments, cancel_appointment
from .department_info import get_department_info, get_visiting_hours
from .emergency import get_emergency_info, get_ambulance_service

__all__ = [
    # Weather & DateTime
    "get_weather",
    "get_current_datetime",
    "get_current_date",
    "get_current_time",
    
    # Doctor & Schedule
    "get_doctor_schedule",
    "check_doctor_availability",
    "list_all_departments",
    
    # Appointments
    "book_appointment",
    "check_patient_appointments",
    "cancel_appointment",
    
    # Department Info
    "get_department_info",
    "get_visiting_hours",
    
    # Emergency
    "get_emergency_info",
    "get_ambulance_service",
]