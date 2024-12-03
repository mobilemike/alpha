"""API client for BlueBubbles."""

from typing import Annotated, Any, Literal
from uuid import uuid4

import httpx
from humps import camelize
from pydantic import UUID4, Field, validate_call

from app.logger import log
from app.settings import settings


@validate_call
def send_text(  # noqa: PLR0913
    chat_guid: Annotated[
        str,
        Field(description="The GUID for the Chat you want this message to be sent to."),
    ],
    message: Annotated[
        str,
        Field(
            description="The message to send.",
        ),
    ],
    *,
    temp_guid: Annotated[
        UUID4,
        Field(
            description=(
                "A unique identifier for the message. This is to prevent duplicate "
                "messages from being sent."
            ),
        ),
    ] = Field(default_factory=uuid4),  # noqa: B008
    method: Annotated[
        Literal["private-api", "apple-script"],
        Field(description="Method to send the message using. Defaults to private-api."),
    ] = "private-api",
    subject: Annotated[
        str | None,
        Field(description="Send a subject with the message. Requires private-api."),
    ] = None,
    effect_id: Annotated[
        Literal[
            "com.apple.MobileSMS.expressivesend.gentle",
            "com.apple.MobileSMS.expressivesend.impact",
            "com.apple.MobileSMS.expressivesend.invisibleink",
            "com.apple.MobileSMS.expressivesend.loud",
            "com.apple.messages.effect.CKConfettiEffect",
            "com.apple.messages.effect.CKEchoEffect",
            "com.apple.messages.effect.CKFireworksEffect",
            "com.apple.messages.effect.CKHappyBirthdayEffect",
            "com.apple.messages.effect.CKHeartEffect",
            "com.apple.messages.effect.CKLasersEffect",
            "com.apple.messages.effect.CKShootingStarEffect",
            "com.apple.messages.effect.CKSparklesEffect",
            "com.apple.messages.effect.CKSpotlightEffect",
        ]
        | None,
        Field(description="Send a message using an effect. Requires private-api."),
    ] = None,
    selected_message_guid: Annotated[
        str | None,
        Field(description="Reply to another message by GUID. Requires private-api."),
    ] = None,
    part_index: Annotated[
        int | None,
        Field(
            description="The part of the message to reply to. macOS Big Sur and newer.",
        ),
    ] = 0,
) -> httpx.Response:
    """Send a message to BlueBubbles."""
    url: str = f"{settings.bb_url}/message/text"
    params: dict[str, str] = {"password": settings.bb_password.get_secret_value()}
    data: dict[str, Any] = camelize(
        {
            "chatGuid": chat_guid,
            "message": message,
            "tempGuid": str(temp_guid),
            "method": method,
            "subject": subject,
            "effectId": effect_id,
            "selected_message_guid": selected_message_guid,
            "partIndex": part_index,
        },
    )

    log.debug(
        "Sending message to BlueBubbles",
        url=url,
        params=params,
        data=data,
    )
    try:
        response: httpx.Response = httpx.post(url, params=params, json=data)
        response.raise_for_status()
    except httpx.RequestError as exc:
        log.exception("Sending message to BlueBubbles failed", exc_info=exc)
    except httpx.HTTPStatusError as exc:
        log.exception(
            "Sending message to BlueBubbles failed",
            code=exc.response.status_code,
            url=exc.request.url,
            exc_info=exc,
        )

    log.info("Message sent", response=response)
    return response
