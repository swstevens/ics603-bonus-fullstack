from fasthtml.common import *
import httpx
from datetime import datetime

API_BASE = "http://localhost:8000"

def render_add_form(users):
    """Form to add new reflections"""
    return Div(
        H2("Add New Reflection"),
        Form(
            Div(
                Label("User:", style="font-weight: bold; margin-right: 10px;"),
                Select(
                    *[Option(f"{u['first_name']} ({u['email']})", value=str(u['id'])) for u in users],
                    name="user_id",
                    required=True
                ),
                style="margin-bottom: 10px;"
            ),
            Input(name="title", placeholder="Title", required=True, style="width: 100%; margin-bottom: 10px;"),
            Textarea(name="text", placeholder="Write your reflection...", required=True,
                    style="width: 100%; height: 200px; margin-bottom: 10px;"),
            Button("Submit", type="submit"),
            hx_post="/api/submit-reflection",
            hx_target="#message",
            hx_swap="innerHTML"
        ),
        Div(id="message")
    )

async def submit_reflection(user_id: int, title: str, text: str):
    """Submit reflection endpoint - classify then create"""
    timestamp = datetime.utcnow().isoformat() + "Z"

    async with httpx.AsyncClient() as client:
        # Step 1: Classify topics
        classify_response = await client.post(
            f"{API_BASE}/api/reflections/classify",
            json={"title": title, "text": text, "timestamp": timestamp, "user_id": user_id}
        )
        topics = classify_response.json()["topics"]

        # Step 2: Create reflection
        await client.post(
            f"{API_BASE}/api/reflections",
            json={"title": title, "text": text, "timestamp": timestamp, "topics": topics, "user_id": user_id}
        )

    return Div(
        P("Reflection submitted successfully!", style="color: green;"),
        A("View Reflections", href="/reflections?user_id=" + str(user_id))
    )
