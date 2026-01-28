"""Emergency handling tools."""

from livekit.agents import function_tool, RunContext


@function_tool()
async def get_emergency_info(
    context: RunContext,
    dummy: str = "",
) -> str:
    """Get emergency contact information and guidance.
    
    Args:
        dummy: Unused parameter (ignore this)
    """
    return """EMERGENCY INFO:
For life-threatening emergencies: Call 911 IMMEDIATELY

Hospital Emergency Department:
- Phone: +1-229-213-9528
- Location: Building A, Ground Floor
- Open: 24/7

Urgent situations: Chest pain, difficulty breathing, severe bleeding, loss of consciousness, severe burns, stroke symptoms, severe allergic reactions

Non-emergencies: Walk-in clinic (8 AM-10 PM daily, 30-45 min wait)"""


@function_tool()
async def get_ambulance_service(
    context: RunContext,
    dummy: str = "",
) -> str:
    """Get information about ambulance services.
    
    Args:
        dummy: Unused parameter (ignore this)
    """
    return """Ambulance Service:
Hospital Ambulance: +1-229-213-9999 (24/7)
Coverage: 50 km radius
Services: Basic & Advanced Life Support, Cardiac, Neonatal
Response time: 15-20 minutes average

For life-threatening emergencies, also call 911."""