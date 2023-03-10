"""Stream type classes for tap-ongoing."""

import requests
from pathlib import Path
from typing import Any, Dict, Optional

from tap_ongoing.client import OngoingStream

SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")

class PurchaseOrderStream(OngoingStream):
    """Purchase orders coming in to the warehouse."""
    name = "purchase_orders"
    path = "/purchaseOrders"
    primary_keys = ["purchaseOrderId", "articleSystemId"]
    schema_filepath = SCHEMAS_DIR / "purchase_orders.json"

    def get_next_page_token(
        self, response: requests.Response, previous_token: Optional[Any]
    ) -> Optional[Any]:
        """Return a token for identifying next page or None if no more pages."""

        if len(response.json()) == 0:
            return None

        max_previous_id = max([
            order.get("purchaseOrderInfo").get("purchaseOrderId")
                for order in response.json()
        ])
        return max_previous_id + 1

    def get_url_params(
        self, context: Optional[dict], next_page_token: Optional[Any]
    ) -> Dict[str, Any]:
        """Return a dictionary of values to be used in URL parameterization."""
        params: dict = {}
        params["goodsOwnerId"] = self.config.get("goods_owner_id")
        params["lastReceiveTimeFrom"] = self.config.get("last_receive_time_from")
        params["maxPurchaseOrdersToGet"] = self.config.get("max_purchase_orders_to_get")
        params["purchaseOrderIdFrom"] = next_page_token
        params[self.replication_key] = self.replication_key

        return params

class OrderStream(OngoingStream):
    """Orders to be shipped to customer."""
    name = "orders"
    path = "/orders"
    primary_keys = ["orderNumber"]
    schema_filepath = SCHEMAS_DIR / "orders.json"

    def get_next_page_token(
        self, response: requests.Response, previous_token: Optional[Any]
    ) -> Optional[Any]:
        """Return a token for identifying next page or None if no more pages."""

        if len(response.json()) == 0:
            return None

        max_previous_id = max([
            order.get("orderInfo").get("orderId")
                for order in response.json()
        ])
        return max_previous_id + 1

    def get_url_params(
        self, context: Optional[dict], next_page_token: Optional[Any]
    ) -> Dict[str, Any]:
        """Return a dictionary of values to be used in URL parameterization."""
        params: dict = {}
        params["goodsOwnerId"] = self.config.get("goods_owner_id")
        params["orderCreatedTimeFrom"] = self.config.get("order_created_time_from")
        params["maxOrdersToGet"] = self.config.get("max_orders_to_get")
        params["orderIdFrom"] = next_page_token

        return params

class ArticleItemStream(OngoingStream):
    """Detailed information about articles in stock."""
    name = "article_items"
    path = "/articleItems"
    primary_keys = ["articleSystemId", "articleNumber"]
    schema_filepath = SCHEMAS_DIR / "article_items.json"

    def get_next_page_token(
        self, response: requests.Response, previous_token: Optional[Any]
    ) -> Optional[Any]:
        """Return a token for identifying next page or None if no more pages."""

        if len(response.json()) == 0:
            return None

        max_previous_id = max([
            article.get("articleSystemId") for article in response.json()
        ])
        return max_previous_id + 1

    def get_url_params(
        self, context: Optional[dict], next_page_token: Optional[Any]
    ) -> Dict[str, Any]:
        """Return a dictionary of values to be used in URL parameterization."""
        params: dict = {}
        params["goodsOwnerId"] = self.config.get("goods_owner_id")
        params["maxArticlesToGet"] = self.config.get("max_articles_to_get")
        params["articleSystemIdFrom"] = next_page_token

        return params
