from fasthtml.common import *
import httpx

API_BASE = "http://localhost:8000"

async def get_reflections(user_id):
    """Fetch reflections by user"""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{API_BASE}/api/reflections?user_id={user_id}")
        return response.json()

async def render_reflections_list(user_id, users):
    """Reflections list table with user filter"""
    reflections = await get_reflections(user_id)

    return Div(
        H2("My Reflections"),
        Div(
            Label("Filter by User:", style="font-weight: bold; margin-right: 10px;"),
            Select(
                *[Option(f"{u['first_name']} ({u['email']})", value=str(u['id']),
                        selected=(u['id'] == user_id)) for u in users],
                hx_get="/reflections",
                hx_target="body",
                hx_trigger="change",
                name="user_id"
            ),
            style="margin-bottom: 20px;"
        ),
        Table(
            Thead(Tr(Th("ID"), Th("Title"), Th("Timestamp"), Th("Topics"))),
            Tbody(
                *[Tr(
                    Td(A(str(r['id']), href=f"/reflection/{r['id']}")),
                    Td(r['title']),
                    Td(r['timestamp']),
                    Td(", ".join(r['topics']))
                ) for r in reflections]
            )
        ) if reflections else P("No reflections yet. Click 'Add Reflection' to create one.")
    )
