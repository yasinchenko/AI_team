# app/services/gen_api.py (использовать настройки)
from app.core.config import settings
import aiohttp

async def send_prompt(messages: list[dict]) -> str:
    headers = {"Authorization": f"Bearer {settings.GEN_API_KEY}"}
    body = {"model_slug": settings.GEN_MODEL_ID, "messages": messages}
    async with aiohttp.ClientSession() as session:
        async with session.post("https://api.gen-api.ru/v1/gen", json=body, headers=headers) as resp:
            data = await resp.json()
            return data["request_id"]

async def poll_result(request_id: str) -> str:
    headers = {"Authorization": f"Bearer {settings.GEN_API_KEY}"}
    async with aiohttp.ClientSession() as session:
        while True:
            async with session.get(f"https://api.gen-api.ru/v1/gen/status?request_id={request_id}", headers=headers) as resp:
                data = await resp.json()
                if data["status"] == "success":
                    return data["result"]