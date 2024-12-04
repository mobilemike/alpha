"""BlueBubbles API Client."""

import httpx
from pydantic import SecretStr

from app.settings import settings

from .message import MessageClient


class BBClient:
    """BlueBubbles API client."""

    def __init__(
        self,
        url: str | None = None,
        password: SecretStr | None = None,
    ) -> None:
        """Initialize the BlueBubbles client."""
        self.url = url or settings.bb_url
        self.password = password or settings.bb_password
        self._message: MessageClient | None = None
        # Create a single httpx client instance
        self.http_client = httpx.Client(timeout=30.0)

    @property
    def message(self) -> MessageClient:
        """Get the message client."""
        if self._message is None:
            self._message = MessageClient(self)
        return self._message

    def get_auth_params(self) -> dict[str, str]:
        """Get the authentication parameters for requests."""
        return {"password": self.password.get_secret_value()}

    def __del__(self) -> None:
        """Clean up the HTTP client when the instance is destroyed."""
        self.http_client.close()
