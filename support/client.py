import httpx
from models.agent import AgentResponse
from support.config import (
    BASE_URL,
    SHIPTEST_CHAT_URL,
    SHIPTEST_LOGIN_URL,
    SHIPTEST_EMAIL,
    SHIPTEST_PASSWORD,
)


def login():
    response = httpx.post(
        BASE_URL + SHIPTEST_LOGIN_URL, # type: ignore
        json={
            "email": SHIPTEST_EMAIL,
            "password": SHIPTEST_PASSWORD,
        },
        timeout=30,
    )
    response.raise_for_status()
    return response.cookies["auth_session"]

def chat(message, history=None, form_context=None):
    response = httpx.post(
        BASE_URL + SHIPTEST_CHAT_URL, # type: ignore
        cookies={"auth_session": login()},
        json={
            "message": message,
            "history": history or [],
            "formContext": form_context,
        },
        timeout=180,
    )
    response.raise_for_status()
    return AgentResponse.model_validate(response.json())