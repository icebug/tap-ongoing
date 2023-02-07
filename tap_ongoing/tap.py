"""Ongoing WMS tap class."""

from typing import List

from singer_sdk import Tap, Stream

from tap_ongoing.streams import (
    PurchaseOrderStream,
    OrderStream,
    ArticleItemStream
)

# TODO
STREAM_TYPES = [
    PurchaseOrderStream,
    OrderStream,
    ArticleItemStream
]

class TapOngoing(Tap):
    """Ongoing tap class."""
    name = "tap-ongoing"

    def discover_streams(self) -> List[Stream]:
        """Return a list of discovered streams."""
        return [stream_class(tap=self) for stream_class in STREAM_TYPES]