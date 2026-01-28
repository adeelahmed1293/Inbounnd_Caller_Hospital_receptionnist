"""Tools for checking doctor schedules and availability."""

from livekit.agents import function_tool, RunContext, ToolError
from database.mongodb import get_doctors_collection, get_appointments_collection
from datetime import datetime
import re


@function_tool()
async def get_doctor_schedule(
    context: RunContext,
    department: str,
    date: str,
) -> str:
    """Get all doctors available in a department on a specific date.
    
    Args:
        department: Department name (e.g., "Cardiology", "Neurology", "General Medicine")
        date: Date in YYYY-MM-DD format (e.g., "2026-01-28")
    """
    try:
        datetime.strptime(date, "%Y-%m-%d")
        day_of_week = datetime.strptime(date, "%Y-%m-%d").strftime("%A")
        
        doctors_collection = get_doctors_collection()
        doctors_cursor = doctors_collection.find({
            "department": {"$regex": f"^{department}$", "$options": "i"}
        })
        
        doctors_list = []
        async for doctor in doctors_cursor:
            doctors_list.append(doctor)
        
        if not doctors_list:
            return f"No doctors found in {department} department. Available departments: Cardiology, Neurology, General Medicine, Pediatrics, Orthopedics."
        
        # More concise, conversational format
        available_doctors = []
        unavailable_doctors = []
        
        for doc in doctors_list:
            working_hours = [wh for wh in doc.get("working_hours", []) 
                           if wh["day"] == day_of_week and wh["is_available"]]
            
            if working_hours:
                wh = working_hours[0]
                available_doctors.append({
                    'name': doc['name'],
                    'specialization': doc['specialization'],
                    'start': wh['start_time'],
                    'end': wh['end_time']
                })
            else:
                unavailable_doctors.append(doc['name'])
        
        if not available_doctors:
            return f"No doctors are available in {department} on {day_of_week}. Please try a different day or department."
        
        # Build concise response
        response = f"{department} doctors available on {day_of_week}, {date}:\n"
        
        for doc in available_doctors:
            response += f"- Dr. {doc['name']} ({doc['specialization']}): {doc['start']}-{doc['end']}\n"
        
        return response.strip()
        
    except ValueError:
        raise ToolError("Invalid date format. Please use YYYY-MM-DD format (e.g., 2026-01-28)")
    except Exception as e:
        raise ToolError(f"Failed to get doctor schedule: {str(e)}")


@function_tool()
async def check_doctor_availability(
    context: RunContext,
    doctor_name: str,
    date: str,
    time: str,
) -> str:
    """Check if a specific doctor is available at a given date and time.
    
    Args:
        doctor_name: Full name of the doctor (e.g., "Dr. Sarah Ahmed")
        date: Date in YYYY-MM-DD format
        time: Time in HH:MM format (24-hour, e.g., "14:30")
    """
    try:
        datetime.strptime(date, "%Y-%m-%d")
        datetime.strptime(time, "%H:%M")
        
        day_of_week = datetime.strptime(date, "%Y-%m-%d").strftime("%A")
        
        doctors_collection = get_doctors_collection()
        appointments_collection = get_appointments_collection()
        
        doctor = await doctors_collection.find_one({
            "name": {"$regex": f"^{doctor_name}$", "$options": "i"}
        })
        
        if not doctor:
            return f"Doctor {doctor_name} not found. Please check the name."
        
        working_hours = [wh for wh in doctor.get("working_hours", []) 
                        if wh["day"] == day_of_week and wh["is_available"]]
        
        if not working_hours:
            return f"Dr. {doctor['name']} is not available on {day_of_week}s."
        
        wh = working_hours[0]
        
        if not (wh["start_time"] <= time <= wh["end_time"]):
            return f"Dr. {doctor['name']} works {wh['start_time']}-{wh['end_time']} on {day_of_week}s. {time} is outside working hours."
        
        existing_appointment = await appointments_collection.find_one({
            "doctor_id": doctor["doctor_id"],
            "date": date,
            "time": time,
            "status": "scheduled"
        })
        
        if existing_appointment:
            return f"Dr. {doctor['name']} is booked at {time} on {date}. Try a different time."
        
        return f"AVAILABLE: Dr. {doctor['name']} is free at {time} on {date}."
        
    except ValueError:
        raise ToolError("Invalid date or time format. Use YYYY-MM-DD for date and HH:MM for time")
    except Exception as e:
        raise ToolError(f"Failed to check availability: {str(e)}")


@function_tool()
async def list_all_departments(
    context: RunContext,
    dummy: str = "",
) -> str:
    """Get a list of all hospital departments with their services.
    
    Args:
        dummy: Unused parameter (ignore this)
    """
    try:
        from database.mongodb import get_departments_collection
        departments_collection = get_departments_collection()
        departments_cursor = departments_collection.find()
        
        departments_list = []
        async for dept in departments_cursor:
            departments_list.append(dept)
        
        if not departments_list:
            return "No departments found in the system."
        
        # More concise format
        response = "Hospital Departments:\n"
        
        for dept in departments_list:
            response += f"\n{dept['name']} - {dept['location']}\n"
            response += f"Phone: {dept['phone']}\n"
            response += f"Services: {', '.join(dept['services'][:3])}"
            if len(dept['services']) > 3:
                response += f" and {len(dept['services']) - 3} more"
            response += "\n"
        
        return response.strip()
        
    except Exception as e:
        raise ToolError(f"Failed to list departments: {str(e)}")