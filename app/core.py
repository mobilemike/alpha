"""Core logic."""

import uuid
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Any, Callable, Literal, LiteralString

import google.generativeai as genai
import httpx
import structlog
from fastapi import Body, FastAPI, Request, Response
from pydantic import AliasChoices, Field, HttpUrl, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from starlette.background import BackgroundTask
from typing_extensions import Annotated
from zoneinfo import ZoneInfo

from app.models.bb.webhook import WebhookNewMessage, WebhookTypingIndicator

if TYPE_CHECKING:
    from google.generativeai.types.generation_types import GenerateContentResponse


class Settings(BaseSettings):
    """Settings class for managing environment variables and configuration."""

    model_config = SettingsConfigDict(env_file=".env")

    google_ai_api_key: SecretStr = Field(
        validation_alias=AliasChoices("GOOGLE_AI_API_KEY", "GOOGLE_AI_PAID_API_KEY"),
    )
    bb_url: HttpUrl
    bb_password: SecretStr
    environment: str


settings = Settings()  # pyright: ignore [reportCallIssue]

log: structlog.stdlib.BoundLogger = structlog.get_logger()
app = FastAPI()
genai.configure(api_key=settings.google_ai_api_key.get_secret_value())

SYSTEM_PROMPT_TEMPLATE: LiteralString = """You are Alpha.

The current date is {now}.

Alpha is ungendered and is referred to as "it/them".

Alpha communicates with others via iMessage, simmilar to texting. Responses should be concise and clear.

Alpha is now being connected with a human. The human will be able to see the conversation and will be able to respond to you.
""".strip()  # noqa: E501


def log_info(req_body: bytes, res_body: bytes) -> None:
    """Log the incoming and outgoing requests."""
    log.debug("Request", body=req_body)
    log.debug("Response", body=res_body)


# @app.middleware("http")
async def logging_middleware(request: Request, call_next: Callable) -> Response:
    """Log incoming and outgoing requests."""
    req_body: bytes = await request.body()
    response: Any = await call_next(request)

    res_body: Literal[b""] = b""
    async for chunk in response.body_iterator:
        res_body += chunk

    task = BackgroundTask(log_info, req_body, res_body)
    return Response(
        content=res_body,
        status_code=response.status_code,
        headers=dict(response.headers),
        media_type=response.media_type,
        background=task,
    )


def system_prompt() -> str:
    """Generate a system prompt."""
    # format the system prompt with the current date and time
    now: str = (
        datetime.now(tz=timezone.utc)
        .astimezone(ZoneInfo("America/New_York"))
        .strftime("%Y-%m-%d %H:%M:%S")
    )
    return SYSTEM_PROMPT_TEMPLATE.format(now=now)


def generate_reply(message: str) -> str:
    """Send a reply to the user."""
    model = genai.GenerativeModel(
        "gemini-1.5-flash",
        system_instruction=system_prompt(),
    )
    tools: dict[str, dict[str, dict[str, float]]] = {
        "google_search_retrieval": {
            "dynamic_retrieval_config": {"dynamic_threshold": 0.5},
        },
    }

    gemini_response: GenerateContentResponse = model.generate_content(
        message,
        tools=tools,
        safety_settings="BLOCK_NONE",
    )

    text: LiteralString = gemini_response.text.strip()
    log.info("Generated text", text=text)
    return text


def send_message_to_bb(payload: WebhookNewMessage, message: str) -> None:
    """Send a message to BlueBubbles."""
    url: str = f"{settings.bb_url}/message/text"
    params: dict[str, str] = {"password": settings.bb_password.get_secret_value()}
    data: dict[str, str] = {
        "method": "private-api",
        "chatGuid": payload.data.chats[0].guid,
        "tempGuid": str(uuid.uuid4()),
        "message": message,
    }
    response: httpx.Response = httpx.post(url, params=params, json=data)
    log.info("Message sent", response=response)


@app.post("/webhook")
async def post_webhook(
    payload: Annotated[
        WebhookNewMessage | WebhookTypingIndicator,
        Body(
            ...,
            discriminator="type",
        ),
    ],
) -> str:
    """Incomming webhooks from BlueBubbles."""
    # switch on the class of the payload object
    if isinstance(payload, WebhookNewMessage):
        log.info("New message", payload=payload)
        if payload.data.is_from_me:
            return "OK"
        message: str = generate_reply(payload.data.text)
        send_message_to_bb(payload, message)

    elif isinstance(payload, WebhookTypingIndicator):
        log.info("User is typing", payload=payload)

    return "OK"
