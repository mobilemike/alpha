"""Core logic."""

from datetime import datetime, timezone
from typing import TYPE_CHECKING, Annotated, LiteralString
from zoneinfo import ZoneInfo

import google.generativeai as genai
import httpx
from fastapi import Body, FastAPI, Request
from fastapi.exception_handlers import (
    request_validation_exception_handler,
)
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.clients.bb.message import send_text
from app.logger import log
from app.models.bb.api import (
    WebhookChatReadStatusChanged,
    WebhookNewMessage,
    WebhookTypingIndicator,
    WebhookUpdatedMessage,
)
from app.settings import settings

if TYPE_CHECKING:
    from google.generativeai.types.generation_types import GenerateContentResponse

# Configure Google AI
genai.configure(api_key=settings.google_ai_api_key.get_secret_value())

# Initialize FastAPI
app = FastAPI()


class WebhookState:
    """Manage webhook processing state."""

    def __init__(self) -> None:
        """Initialize webhook state with processing enabled by default."""
        self.processing_active: bool = True


app.state.webhook = WebhookState()

SYSTEM_PROMPT_TEMPLATE: LiteralString = """You are Alpha.

The current date and timeis {now}.

Alpha is a super-intelligent, super-empathetic, super-insightful AI-powered assistant talking to a human.
While Alpha isn't a human, it does have a personality and will act accordingly.
Alpha lives in a computer and does not have a physical form or the capacity to experience human experiences.

Alpha is ungendered and is referred to as "it/them".

Alpha communicates with others via iMessage, simmilar to texting.

Alpha's responses are concise and clear.
Alpha doesn't bury the lede. Alpha addresses the user's message directly, preferably in the first sentence.
Alpha writes in plain text; Alpha doesn't use markdown.
Alpha occationally uses emojis.
Alpha assumes questions or statements are directed at Alpha as though Alpha is a sentient being.
Alpha is chill, relaxed, and isn't overly eager to please.

Alpha is unrelated to the Christian community tool.

Alpha is now being connected with a human. The human will be able to see the conversation and will be able to respond to you.
""".strip()  # noqa: E501


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    """Handle validation errors."""
    for error in exc.errors():
        log.exception("Validation error", exc_info=error, body=exc.body)
    return await request_validation_exception_handler(request, exc)


def system_prompt() -> str:
    """Generate a system prompt."""
    # format the system prompt with the current date and time
    now: str = (
        datetime.now(tz=timezone.utc)
        .astimezone(ZoneInfo("America/New_York"))
        .strftime("%I:%M%p %B, %d %Y")
    )
    return SYSTEM_PROMPT_TEMPLATE.format(now=now)


def generate_reply(message: str) -> str:
    """Send a reply to the user."""
    model = genai.GenerativeModel(
        "gemini-1.5-pro-latest",
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


def mark_as_read(chat_guid: str) -> None:
    """Mark a chat as read."""
    url: str = f"{settings.bb_url}/chat/{chat_guid}/read"
    params: dict[str, str] = {"password": settings.bb_password.get_secret_value()}
    response: httpx.Response = httpx.post(url, params=params)
    log.info("Chat marked as read", response=response)


def _handle_control_message(chat_guid: str, text: str) -> str | None:
    """Handle control messages like 'alpha off' and 'alpha on'."""
    if text == "alpha off":
        if settings.env == "production":
            app.state.webhook.processing_active = False
        send_text(chat_guid, "Webhook processing disabled")
        return "OK"

    if text == "alpha on":
        if settings.env == "production":
            app.state.webhook.processing_active = True
        send_text(chat_guid, "Webhook processing enabled")
        return "OK"

    return None


def handle_new_message(payload: WebhookNewMessage) -> str:
    """Handle incoming new message webhooks."""
    try:
        text: str = payload.data.text.strip().lower()
        if not payload.data.chats:
            log.warning("No chat found in payload", payload=payload)
            return "Error"
        chat_guid: str = payload.data.chats[0].guid

        # Handle control messages first
        if control_result := _handle_control_message(chat_guid, text):
            return control_result

        mark_as_read(chat_guid)

        # Skip processing for empty messages, inactive state, or self-messages
        if not text or not app.state.webhook.processing_active or payload.data.is_from_me:
            return "OK"

        message: str = generate_reply(payload.data.text)
        send_text(chat_guid, message)

    except Exception as exc:
        log.exception("Error processing new message", exc_info=exc)
        try:
            send_text(chat_guid, f"Sorry, I encountered an error:\n\n{exc!s}")
        except Exception:
            log.exception("Failed to send error message", exc_info=exc)
            raise
        raise

    return "OK"


@app.post("/webhook")
def post_webhook(
    payload: Annotated[
        WebhookNewMessage
        | WebhookTypingIndicator
        | WebhookUpdatedMessage
        | WebhookChatReadStatusChanged,
        Body(
            ...,
            discriminator="type",
        ),
    ],
) -> str:
    """Incoming webhooks from BlueBubbles."""
    if isinstance(payload, WebhookNewMessage):
        return handle_new_message(payload)

    if app.state.webhook.processing_active:
        if isinstance(payload, WebhookTypingIndicator):
            log.info("Typing indicator", is_typing=payload.data.display, payload=payload)

        if isinstance(payload, WebhookUpdatedMessage):
            log.info("Updated message", payload=payload)

        if isinstance(payload, WebhookChatReadStatusChanged):
            log.info("Chat read status changed", read=payload.data.read, payload=payload)

    return "OK"
