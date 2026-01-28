"""Tools for booking and managing appointments."""

from livekit.agents import function_tool, RunContext, ToolError
from database.mongodb import get_appointments_collection, get_doctors_collection, get_patients_collection
from datetime import datetime
import uuid


@function_tool()
async def book_appointment(
    context: RunContext,
    patient_name: str,
    patient_phone: str,
    doctor_name: str,
    date: str,
    time: str,
    reason: str,
) -> str:
    """Book an appointment for a patient with a doctor.
    
    Args:
        patient_name: Full name of the patient
        patient_phone: Patient's phone number
        doctor_name: Full name of the doctor
        date: Appointment date in YYYY-MM-DD format
        time: Appointment time in HH:MM format (24-hour)
        reason: Reason for visit (e.g., "Regular checkup", "Follow-up", "Consultation")
    """
    try:
        datetime.strptime(date, "%Y-%m-%d")
        datetime.strptime(time, "%H:%M")
        
        doctors_collection = get_doctors_collection()
        appointments_collection = get_appointments_collection()
        patients_collection = get_patients_collection()
        
        doctor = await doctors_collection.find_one({
            "name": {"$regex": f"^{doctor_name}$", "$options": "i"}
        })
        
        if not doctor:
            return f"Doctor {doctor_name} not found. Please check the name."
        
        existing = await appointments_collection.find_one({
            "doctor_id": doctor["doctor_id"],
            "date": date,
            "time": time,
            "status": "scheduled"
        })
        
        if existing:
            return f"Time slot {time} on {date} is already booked. Please choose a different time."
        
        patient = await patients_collection.find_one({"phone": patient_phone})
        
        if not patient:
            patient_id = str(uuid.uuid4())
            patient = {
                "patient_id": patient_id,
                "name": patient_name,
                "phone": patient_phone,
            }
            await patients_collection.insert_one(patient)
        else:
            patient_id = patient["patient_id"]
        
        appointment_id = str(uuid.uuid4())
        appointment = {
            "appointment_id": appointment_id,
            "patient_id": patient_id,
            "patient_name": patient_name,
            "patient_phone": patient_phone,
            "doctor_id": doctor["doctor_id"],
            "doctor_name": doctor["name"],
            "department": doctor["department"],
            "date": date,
            "time": time,
            "reason": reason,
            "status": "scheduled",
            "created_at": datetime.now().isoformat()
        }
        
        await appointments_collection.insert_one(appointment)
        
        # More concise, conversational response
        return f"""BOOKING CONFIRMED
ID: {appointment_id[:8]}
Patient: {patient_name}
Doctor: Dr. {doctor['name']} ({doctor['department']})
When: {date} at {time}
Reason: {reason}
Note: Please arrive 15 minutes early with ID and insurance card."""
        
    except ValueError:
        raise ToolError("Invalid date or time format. Use YYYY-MM-DD for date and HH:MM for time")
    except Exception as e:
        raise ToolError(f"Failed to book appointment: {str(e)}")


@function_tool()
async def check_patient_appointments(
    context: RunContext,
    patient_phone: str,
) -> str:
    """Check all appointments for a patient using their phone number.
    
    Args:
        patient_phone: Patient's phone number
    """
    try:
        appointments_collection = get_appointments_collection()
        
        appointments_cursor = appointments_collection.find({
            "patient_phone": patient_phone,
            "status": "scheduled"
        }).sort("date", 1)
        
        appointments = []
        async for apt in appointments_cursor:
            appointments.append(apt)
        
        if not appointments:
            return f"No scheduled appointments found for {patient_phone}."
        
        # More concise format
        response = f"Appointments for {patient_phone}:\n"
        
        for i, apt in enumerate(appointments, 1):
            response += f"\n{i}. {apt['date']} at {apt['time']}\n"
            response += f"   Dr. {apt['doctor_name']} ({apt['department']})\n"
            response += f"   ID: {apt['appointment_id'][:8]} | Reason: {apt['reason']}\n"
        
        return response.strip()
        
    except Exception as e:
        raise ToolError(f"Failed to check appointments: {str(e)}")


@function_tool()
async def cancel_appointment(
    context: RunContext,
    appointment_id: str,
    patient_phone: str,
) -> str:
    """Cancel an existing appointment.
    
    Args:
        appointment_id: The appointment ID (first 8 characters)
        patient_phone: Patient's phone number for verification
    """
    try:
        appointments_collection = get_appointments_collection()
        
        appointment = await appointments_collection.find_one({
            "appointment_id": {"$regex": f"^{appointment_id}"},
            "patient_phone": patient_phone,
            "status": "scheduled"
        })
        
        if not appointment:
            return f"No appointment found with ID {appointment_id} for {patient_phone}."
        
        await appointments_collection.update_one(
            {"appointment_id": appointment["appointment_id"]},
            {"$set": {"status": "cancelled"}}
        )
        
        # More concise response
        return f"""CANCELLED
ID: {appointment_id}
Patient: {appointment['patient_name']}
Dr. {appointment['doctor_name']}
Was scheduled: {appointment['date']} at {appointment['time']}
You can book a new appointment anytime."""
        
    except Exception as e:
        raise ToolError(f"Failed to cancel appointment: {str(e)}")