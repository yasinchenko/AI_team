# app/services/dispatcher.py
from app.services.gen_api import send_prompt, poll_result

async def route_task_to_agent(task: dict) -> str:
    prompt = [
        {"role": "system", "content": "Ты — эксперт по FastAPI и микросервисам."},
        {"role": "user", "content": f"Сгенерируй код для задачи: {task['title']}\n\n{task.get('description', '')}"}
    ]
    request_id = await send_prompt(prompt)
    result = await poll_result(request_id)
    return result
