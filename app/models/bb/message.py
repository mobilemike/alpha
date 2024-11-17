"""Pydantic models for outgoing requests to BB."""

from typing import Literal
from uuid import UUID, uuid4

from pydantic import UUID4, BaseModel, Field


class Text(BaseModel):
    """Text model."""

    chat_guid: UUID = Field(alias="chatGuid")
    temp_guid: UUID4 = Field(alias="tempGuid", default_factory=uuid4)
    message: str
    method: Literal["private-api", "apple-script"] = "private-api"
    subject: str | None
    effect_id: str | None = Field(alias="effectId")
    selected_message_guid: UUID | None = Field(alias="selectedMessageGuid")
    part_index: int | None
