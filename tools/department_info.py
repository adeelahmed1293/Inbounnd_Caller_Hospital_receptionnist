"""Tools for department information."""

from livekit.agents import function_tool, RunContext, ToolError
from database.mongodb import get_departments_collection


@function_tool()
async def get_department_info(
    context: RunContext,
    department_name: str,
) -> str:
    """Get detailed information about a specific department.
    
    Args:
        department_name: Name of the department (e.g., "Cardiology", "Emergency")
    """
    try:
        departments_collection = get_departments_collection()
        
        department = await departments_collection.find_one({
            "name": {"$regex": f"^{department_name}$", "$options": "i"}
        })
        
        if not department:
            return f"Department {department_name} not found. Use list_all_departments to see available departments."
        
        # More concise, conversational format
        response = f"{department['name']} Department\n"
        response += f"Location: {department['location']}\n"
        response += f"Phone: {department['phone']}\n"
        response += f"\nKey Services: {', '.join(department['services'][:4])}"
        if len(department['services']) > 4:
            response += f" and {len(department['services']) - 4} more"
        
        return response.strip()
        
    except Exception as e:
        raise ToolError(f"Failed to get department info: {str(e)}")


@function_tool()
async def get_visiting_hours(
    context: RunContext,
    dummy: str = "",
) -> str:
    """Get hospital visiting hours and policies.
    
    Args:
        dummy: Unused parameter (ignore this)
    """
    return """Visiting Hours:
General Wards: 10 AM-12 PM, 4 PM-7 PM
ICU: 11-11:30 AM, 5-5:30 PM (max 2 visitors)
Emergency: 24/7 (one guardian)

Rules: Hand sanitization required, phones on silent, max 2 visitors per patient, children under 12 not allowed in ICU."""