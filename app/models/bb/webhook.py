"""Pydantic models for incoming webhooks from BB."""

from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field


class Handle(BaseModel):
    """Handle model."""

    original_rowid: int = Field(alias="originalROWID")
    address: str
    service: str
    uncanonical_id: str | None = Field(alias="uncanonicalizedId")
    country: str


class Chat(BaseModel):
    """Chat model."""

    original_rowid: int = Field(alias="originalROWID")
    guid: UUID
    style: int
    chat_identifier: str = Field(alias="chatIdentifier")
    is_archived: bool = Field(alias="isArchived")
    display_name: str = Field(alias="displayName")


class AttachementMetadata(BaseModel):
    """Attachment metadata model."""

    size: int
    height: int
    width: int


class Attachememt(BaseModel):
    """Attachment model."""

    original_rowid: int = Field(alias="originalROWID")
    guid: UUID
    uti: str
    mime_type: str = Field(alias="mimeType")
    transfer_name: str = Field(alias="transferName")
    total_bytes: int = Field(alias="totalBytes")
    height: int
    width: int
    metadata: AttachementMetadata


class WebhookNewMessageData(BaseModel):
    """Webhook data model."""

    original_rowid: int = Field(alias="originalROWID")
    guid: UUID
    text: str
    attributed_body: str | None = Field(alias="attributedBody")
    handle: Handle
    handle_id: int = Field(alias="handleId")
    other_handle: int = Field(alias="otherHandle")
    attachments: list[Attachememt]
    subject: str | None
    error: int
    date_created: datetime = Field(alias="dateCreated")
    date_read: datetime | None = Field(alias="dateRead")
    date_delivered: datetime | None = Field(alias="dateDelivered")
    is_from_me: bool = Field(alias="isFromMe")
    has_dd_results: bool = Field(alias="hasDdResults")
    is_archived: bool = Field(alias="isArchived")
    item_type: int = Field(alias="itemType")
    group_title: str | None = Field(alias="groupTitle")
    group_action_type: int = Field(alias="groupActionType")
    balloon_bundle_id: str | None = Field(alias="balloonBundleId")
    associated_message_guid: str | None = Field(alias="associatedMessageGuid")
    associated_message_type: str | None = Field(alias="associatedMessageType")
    expressive_send_style_id: str | None = Field(alias="expressiveSendStyleId")
    thread_originator_guid: str | None = Field(alias="threadOriginatorGuid")
    has_payload_data: bool = Field(alias="hasPayloadData")
    chats: list[Chat]
    message_summary_info: dict | None = Field(alias="messageSummaryInfo")
    payload_data: dict | None = Field(alias="payloadData")


class WebhookNewMessage(BaseModel):
    """Webhook model for new messages."""

    type: Literal["new-message"]
    data: WebhookNewMessageData


class WebhookTypingIndicatorData(BaseModel):
    """Webhook data model for typing indicators."""

    display: bool
    guid: str


class WebhookTypingIndicator(BaseModel):
    """Webhook model for typing indicators."""

    type: Literal["typing-indicator"]
    data: WebhookTypingIndicatorData
