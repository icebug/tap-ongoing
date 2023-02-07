"""REST client handling, including OngoingStream base class."""

from pathlib import Path

from singer_sdk.streams import RESTStream
from singer_sdk.authenticators import BasicAuthenticator


SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")


class OngoingStream(RESTStream):
    """Ongoing stream class."""

    url_base = "https://api.ongoingsystems.se/Storex/api/v1"

    records_jsonpath = "$[*]"

    @property
    def authenticator(self) -> BasicAuthenticator:
        """Return a new authenticator object."""
        return BasicAuthenticator.create_for_stream(
            self,
            username=self.config.get("username"),
            password=self.config.get("password"),
        )

    @property
    def http_headers(self) -> dict:
        """Return the http headers needed."""
        headers = {}
        if "user_agent" in self.config:
            headers["User-Agent"] = self.config.get("user_agent")
        # If not using an authenticator, you may also provide inline auth headers:
        # headers["Private-Token"] = self.config.get("auth_token")
        return headers
