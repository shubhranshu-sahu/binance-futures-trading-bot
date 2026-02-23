from bot.client import BinanceFuturesClient
from bot.logging_config import setup_logger

logger = setup_logger()


class OrderService:
    def __init__(self):
        self.client = BinanceFuturesClient()

    def place_market_order(self, symbol: str, side: str, quantity: float):
        params = {
            "symbol": symbol.upper(),
            "side": side.upper(),
            "type": "MARKET",
            "quantity": quantity
        }

        logger.info(f"Placing MARKET order: {params}")

        response = self.client._send_request(
            "POST",
            "/fapi/v1/order",
            params
        )

        return response

    def place_limit_order(self, symbol: str, side: str, quantity: float, price: float):
        params = {
            "symbol": symbol.upper(),
            "side": side.upper(),
            "type": "LIMIT",
            "quantity": quantity,
            "price": price,
            "timeInForce": "GTC"
        }

        logger.info(f"Placing LIMIT order: {params}")

        response = self.client._send_request(
            "POST",
            "/fapi/v1/order",
            params
        )

        return response