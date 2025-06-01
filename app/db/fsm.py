# app/db/fsm.py
TASK_STATES = [
    "created",
    "assigned",
    "waiting_approval",
    "approved",
    "done",
    "rejected"
]

def get_next_state(current: str) -> str:
    try:
        idx = TASK_STATES.index(current)
        return TASK_STATES[idx + 1]
    except (ValueError, IndexError):
        raise ValueError(f"Invalid or final state: {current}")

def is_final_state(state: str) -> bool:
    return state in ("done", "rejected")

def reset_state() -> str:
    return TASK_STATES[0]