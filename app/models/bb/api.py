"""Pydantic models for incoming webhooks from BB."""

from datetime import datetime
from typing import Any, Literal
from uuid import UUID, uuid4

from humps import camelize
from pydantic import UUID4, BaseModel, ConfigDict, Field

# Base models


class BaseBBModel(BaseModel):
    """Base model for BB models."""

    model_config = ConfigDict(alias_generator=camelize, populate_by_name=True)


class Handle(BaseBBModel):
    """Handle model."""

    original_rowid: int = Field(alias="originalROWID")
    address: str
    service: str
    uncanonicalized_id: str | None
    country: str


class Chat(BaseBBModel):
    """Chat model."""

    original_rowid: int = Field(alias="originalROWID")
    guid: str
    style: int
    chat_identifier: str
    is_archived: bool
    display_name: str


class AttachmentMetadata(BaseBBModel):
    """Attachment metadata model."""

    size: int | None
    height: int
    width: int


class Attachmemt(BaseBBModel):
    """Attachment model."""

    original_rowid: int = Field(alias="originalROWID")
    guid: UUID
    uti: str
    mime_type: str
    transfer_name: str
    total_bytes: int
    height: int
    width: int
    metadata: AttachmentMetadata


class Message(BaseBBModel):
    """Base webhook data model."""

    original_rowid: int = Field(alias="originalROWID")
    guid: UUID
    text: str
    attributed_body: str | None
    handle: Handle
    handle_id: int
    other_handle: int
    attachments: list[Attachmemt]
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
    country: str | None = None
    is_delayed: bool | None = None
    is_auto_reply: bool | None = None
    is_system_message: bool | None = None
    is_service_message: bool | None = None
    is_forward: bool | None = None
    thread_originator_part: Any | None = None
    is_corrupt: bool | None = None
    date_played: int | None = None
    cache_roomnames: Any | None = None
    is_spam: bool | None = None
    is_expired: bool | None = None
    time_expressive_send_played: int | None = None
    is_audio_message: bool | None = None
    reply_to_guid: str | None = None
    share_status: Any | None = None
    share_direction: Any | None = None
    was_delivered_quietly: bool | None = None
    did_notify_recipient: bool | None = None
    chats: list[Chat] | None = None
    date_edited: int | None = None
    date_retracted: int | None = None
    part_count: int | None = None
    message_summary_info: dict | None = None
    payload_data: dict | None = None


# Webhook models


class WebhookNewMessage(BaseBBModel):
    """Webhook model for new messages."""

    type: Literal["new-message"]
    data: Message


class WebhookUpdatedMessage(BaseBBModel):
    """Webhook model for new messages."""

    type: Literal["updated-message"]
    data: Message


class WebhookTypingIndicatorData(BaseBBModel):
    """Webhook data model for typing indicators."""

    display: bool
    guid: str


class WebhookTypingIndicator(BaseBBModel):
    """Webhook model for typing indicators."""

    type: Literal["typing-indicator"]
    data: WebhookTypingIndicatorData


class WebhookChatReadStatusChangedData(BaseBBModel):
    """Webhook data model for chat read status changed."""

    chat_guid: str
    read: bool


class WebhookChatReadStatusChanged(BaseBBModel):
    """Webhook model for chat read status changed."""

    type: Literal["chat-read-status-changed"]
    data: WebhookChatReadStatusChangedData


# API request models


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


# API response models


class ResponseMetadata(BaseBBModel):
    """Response metadata model."""

    offset: int
    limit: int
    total: int
    count: int


class BaseResponse(BaseBBModel):
    """Base response model."""

    metadata: ResponseMetadata
    status: int
    message: str


class MessagesResponse(BaseResponse):
    """Messages response model."""

    data: list[Message]
