from dotenv import load_dotenv
from livekit.plugins import cartesia, groq, deepgram
from livekit import agents, rtc
from livekit.agents import AgentServer, AgentSession, Agent, room_io
from livekit.plugins import noise_cancellation, silero
from livekit.plugins.turn_detector.multilingual import MultilingualModel

# Import all tools
from tools import (
    # Weather & DateTime
    get_weather,
    get_current_datetime,
    get_current_date,
    get_current_time,
    
    # Doctor & Schedule
    get_doctor_schedule,
    check_doctor_availability,
    list_all_departments,
    
    # Appointments
    book_appointment,
    check_patient_appointments,
    cancel_appointment,
    
    # Department Info
    get_department_info,
    get_visiting_hours,
    
    # Emergency
    get_emergency_info,
    get_ambulance_service,
)

# Import prompts
from prompts import ASSISTANT_INSTRUCTIONS, GREETING_INSTRUCTIONS

# Import database
from database.mongodb import MongoDB

load_dotenv()


class HospitalReceptionist(Agent):
    def __init__(self) -> None:
        super().__init__(
            instructions=ASSISTANT_INSTRUCTIONS,
            tools=[
                # Weather & DateTime
                get_weather,
                get_current_datetime,
                get_current_date,
                get_current_time,
                
                # Doctor & Schedule
                get_doctor_schedule,
                check_doctor_availability,
                list_all_departments,
                
                # Appointments
                book_appointment,
                check_patient_appointments,
                cancel_appointment,
                
                # Department Info
                get_department_info,
                get_visiting_hours,
                
                # Emergency
                get_emergency_info,
                get_ambulance_service,
            ],
        )


server = AgentServer()


@server.rtc_session()
async def receptionist_agent(ctx: agents.JobContext):
    # Connect to MongoDB (synchronous - no await)
    await MongoDB.connect()  # ← REMOVED await
    
    session = AgentSession(
        stt=deepgram.STTv2(
            model="flux-general-en",
            eager_eot_threshold=0.4,
        ),
        llm=groq.LLM(
            model="openai/gpt-oss-120b"
        ),
        tts=cartesia.TTS(
            model="sonic-3",
            voice="f786b574-daa5-4673-aa0c-cbe3e8534c02",
        ),
        vad=silero.VAD.load(),
        turn_detection=MultilingualModel(),
    )

    await session.start(
        room=ctx.room,
        agent=HospitalReceptionist(),
        room_options=room_io.RoomOptions(
            audio_input=room_io.AudioInputOptions(
                noise_cancellation=lambda params: noise_cancellation.BVCTelephony() 
                    if params.participant.kind == rtc.ParticipantKind.PARTICIPANT_KIND_SIP 
                    else noise_cancellation.BVC(),
            ),
        ),
    )

    await session.generate_reply(
        instructions=GREETING_INSTRUCTIONS
    )


if __name__ == "__main__":
    agents.cli.run_app(server)