"""Pydantic models for incoming webhooks from BB."""

from datetime import datetime
from typing import Literal
from uuid import UUID

from humps import camelize
from pydantic import BaseModel, ConfigDict, Field


class Handle(BaseModel):
    """Handle model."""

    model_config = ConfigDict(alias_generator=camelize, populate_by_name=True)

    original_rowid: int = Field(alias="originalROWID")
    address: str
    service: str
    uncanonicalized_id: str | None
    country: str


class Chat(BaseModel):
    """Chat model."""

    model_config = ConfigDict(alias_generator=camelize, populate_by_name=True)

    original_rowid: int = Field(alias="originalROWID")
    guid: str
    style: int
    chat_identifier: str
    is_archived: bool
    display_name: str


class AttachementMetadata(BaseModel):
    """Attachment metadata model."""

    model_config = ConfigDict(alias_generator=camelize, populate_by_name=True)

    size: int | None
    height: int
    width: int


class Attachememt(BaseModel):
    """Attachment model."""

    model_config = ConfigDict(alias_generator=camelize, populate_by_name=True)

    original_rowid: int = Field(alias="originalROWID")
    guid: UUID
    uti: str
    mime_type: str
    transfer_name: str
    total_bytes: int
    height: int
    width: int
    metadata: AttachementMetadata


class BaseWebhookMessageData(BaseModel):
    """Base webhook data model."""

    model_config = ConfigDict(alias_generator=camelize, populate_by_name=True)

    original_rowid: int = Field(alias="originalROWID")
    guid: UUID
    text: str
    attributed_body: str | None
    handle: Handle
    handle_id: int
    other_handle: int
    attachments: list[Attachememt]
    subject: str | None
    error: int
    date_created: datetime
    date_read: datetime | None
    date_delivered: datetime | None
    is_from_me: bool
    has_dd_results: bool
    is_archived: bool
    item_type: int
    group_title: str | None
    group_action_type: int
    balloon_bundle_id: str | None
    associated_message_guid: str | None
    associated_message_type: str | None
    expressive_send_style_id: str | None
    thread_originator_guid: str | None
    has_payload_data: bool
    message_summary_info: dict | None
    payload_data: dict | None


class WebhookNewMessageData(BaseWebhookMessageData):
    """Webhook data model for new messages."""

    chats: list[Chat]


class WebhookNewMessage(BaseModel):
    """Webhook model for new messages."""

    model_config = ConfigDict(alias_generator=camelize, populate_by_name=True)

    type: Literal["new-message"]
    data: WebhookNewMessageData


class WebhookUpdatedMessage(BaseModel):
    """Webhook model for new messages."""

    model_config = ConfigDict(alias_generator=camelize, populate_by_name=True)

    type: Literal["updated-message"]
    data: BaseWebhookMessageData


class WebhookTypingIndicatorData(BaseModel):
    """Webhook data model for typing indicators."""

    model_config = ConfigDict(alias_generator=camelize, populate_by_name=True)

    display: bool
    guid: str


class WebhookTypingIndicator(BaseModel):
    """Webhook model for typing indicators."""

    model_config = ConfigDict(alias_generator=camelize, populate_by_name=True)

    type: Literal["typing-indicator"]
    data: WebhookTypingIndicatorData


class WebhookChatReadStatusChangedData(BaseModel):
    """Webhook data model for chat read status changed."""

    model_config = ConfigDict(alias_generator=camelize, populate_by_name=True)

    chat_guid: str
    read: bool


class WebhookChatReadStatusChanged(BaseModel):
    """Webhook model for chat read status changed."""

    model_config = ConfigDict(alias_generator=camelize, populate_by_name=True)

    type: Literal["chat-read-status-changed"]
    data: WebhookChatReadStatusChangedData
