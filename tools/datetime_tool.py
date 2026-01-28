"""DateTime tools for getting current date and time information."""

from livekit.agents import function_tool, RunContext, ToolError
from datetime import datetime
import pytz


@function_tool()
async def get_current_datetime(
    context: RunContext,
    timezone: str = "UTC",
) -> str:
    """Get the current date and time.
    
    Args:
        timezone: Timezone name (e.g., "UTC", "Asia/Karachi", "America/New_York", "Europe/London")
    """
    try:
        tz = pytz.timezone(timezone)
        now = datetime.now(tz)
        return f"The current date and time in {timezone} is {now.strftime('%A, %B %d, %Y at %I:%M %p')}"
    except pytz.exceptions.UnknownTimeZoneError:
        now = datetime.now(pytz.UTC)
        return f"Unknown timezone '{timezone}'. The current UTC time is {now.strftime('%A, %B %d, %Y at %I:%M %p')}"
    except Exception as e:
        raise ToolError(f"Failed to get date/time: {str(e)}")


@function_tool()
async def get_current_date(
    context: RunContext,
    dummy: str = "",  # ← ADD a dummy parameter
) -> str:
    """Get today's date.
    
    Args:
        dummy: Unused parameter (ignore this)
    """
    now = datetime.now()
    return f"Today is {now.strftime('%A, %B %d, %Y')}"


@function_tool()
async def get_current_time(
    context: RunContext,
    timezone: str = "UTC",
) -> str:
    """Get the current time.
    
    Args:
        timezone: Timezone name (e.g., "UTC", "Asia/Karachi", "America/New_York", "Europe/London")
    """
    try:
        tz = pytz.timezone(timezone)
        now = datetime.now(tz)
        return f"The current time in {timezone} is {now.strftime('%I:%M %p')}"
    except pytz.exceptions.UnknownTimeZoneError:
        now = datetime.now(pytz.UTC)
        return f"Unknown timezone '{timezone}'. The current UTC time is {now.strftime('%I:%M %p')}"
    except Exception as e:
        raise ToolError(f"Failed to get time: {str(e)}")