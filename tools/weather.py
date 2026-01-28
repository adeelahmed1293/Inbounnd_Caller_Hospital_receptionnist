"""Weather tool for getting current weather information."""

from livekit.agents import function_tool, RunContext, ToolError
import os


@function_tool()
async def get_weather(
    context: RunContext,
    city: str,
) -> str:
    """Get the current weather for a specific city.
    
    Args:
        city: Name of the city (e.g., "London", "New York", "Islamabad")
    """
    # Mock response - replace with real API call
    # To use real weather data:
    # 1. Sign up at https://openweathermap.org/api
    # 2. Add WEATHER_API_KEY to your .env file
    # 3. Uncomment the code below
    
    WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
    
    if WEATHER_API_KEY:
        import aiohttp
        try:
            async with aiohttp.ClientSession() as session:
                url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
                async with session.get(url) as resp:
                    if resp.status != 200:
                        raise ToolError(f"Could not fetch weather for {city}")
                    data = await resp.json()
                    temp = data['main']['temp']
                    desc = data['weather'][0]['description']
                    humidity = data['main']['humidity']
                    return f"The weather in {city} is {desc} with a temperature of {temp} degrees Celsius and {humidity}% humidity"
        except Exception as e:
            raise ToolError(f"Failed to get weather data: {str(e)}")
    
    # Mock response when no API key
    return f"The weather in {city} is sunny with a temperature of 25 degrees Celsius. This is a demo response. Add your weather API key to get real data."