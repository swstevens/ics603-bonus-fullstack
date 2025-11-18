from fasthtml.common import *
import httpx
from components.add_form import render_add_form, submit_reflection
from components.reflections_list import render_reflections_list
from components.single_reflection import render_single_reflection

app, rt = fast_app()

API_BASE = "http://localhost:8000"

async def get_users():
    """Fetch all users"""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{API_BASE}/api/users")
        return response.json()

# Home page with title and tabs
@rt("/")
async def get():
    users = await get_users()
    return Titled("Reflection Manager",
        H1("Reflection Manager"),
        Div(
            A("Add Reflection", href="/", style="margin-right: 20px; font-weight: bold;"),
            A("View Reflections", href="/reflections", style="font-weight: bold;"),
            style="margin-bottom: 20px;"
        ),
        render_add_form(users)
    )

# Submit reflection endpoint
@rt("/api/submit-reflection")
async def post(user_id: int, title: str, text: str):
    return await submit_reflection(user_id, title, text)

# Reflections list page
@rt("/reflections")
async def get(user_id: int = 0):
    users = await get_users()
    return Titled("My Reflections",
        H1("Reflection Manager"),
        Div(
            A("← Back to Home", href="/", style="margin-bottom: 20px; display: block;"),
        ),
        await render_reflections_list(user_id, users)
    )

# Single reflection page
@rt("/reflection/{reflection_id}")
async def get(reflection_id: int):
    return Titled("Reflection Detail",
        H1("Reflection Manager"),
        A("← Back to Reflections", href="/reflections", style="margin-bottom: 20px; display: block;"),
        await render_single_reflection(reflection_id)
    )

serve()
