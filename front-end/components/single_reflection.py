from fasthtml.common import *
import httpx

API_BASE = "http://localhost:8000"

async def get_reflection(reflection_id):
    """Fetch single reflection"""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{API_BASE}/api/reflections/{reflection_id}")
        return response.json()

async def render_single_reflection(reflection_id):
    """Single reflection detail view"""
    reflection = await get_reflection(reflection_id)

    return Div(
        H2(reflection.get('title', '')),
        P(reflection.get('timestamp', ''), style="color: gray;"),
        P(reflection.get('text', '')),
        Div(
            Strong("Topics: "),
            *[Span(topic, style="margin-right: 5px; padding: 5px; background: #e0e0e0; border-radius: 3px;")
              for topic in reflection.get('topics', [])]
        )
    )
