"""Pydantic models for outgoing requests to BB."""

from typing import Literal
from uuid import uuid4

from humps import camelize
from pydantic import UUID4, BaseModel, ConfigDict, Field


class Text(BaseModel):
    """Text model."""

    model_config = ConfigDict(alias_generator=camelize, populate_by_name=True)

    chat_guid: str
    temp_guid: UUID4 = Field(default_factory=uuid4)
    message: str
    method: Literal["private-api", "apple-script"] = "private-api"
    subject: str | None = None
    effect_id: str | None = None
    selected_message_guid: str | None = None
    part_index: int | None = None
