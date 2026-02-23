import os
import time
import hmac
import hashlib
import requests
from urllib.parse import urlencode
from dotenv import load_dotenv

from bot.logging_config import setup_logger

load_dotenv()

logger = setup_logger()


class BinanceFuturesClient:
    def __init__(self):
        self.api_key = os.getenv("BINANCE_API_KEY")
        self.secret_key = os.getenv("BINANCE_SECRET_KEY")
        self.base_url = os.getenv("BASE_URL")

        if not self.api_key or not self.secret_key:
            raise ValueError("API Key or Secret Key not found in environment variables.")

    def _get_timestamp(self):
        return int(time.time() * 1000)

    def _sign(self, query_string: str) -> str:
        return hmac.new(
            self.secret_key.encode("utf-8"),
            query_string.encode("utf-8"),
            hashlib.sha256
        ).hexdigest()

    def _send_request(self, method: str, endpoint: str, params: dict):
        try:
            params["timestamp"] = self._get_timestamp()

            query_string = urlencode(params)
            signature = self._sign(query_string)

            params["signature"] = signature

            headers = {
                "X-MBX-APIKEY": self.api_key
            }

            url = f"{self.base_url}{endpoint}"

            logger.info(f"Sending {method} request to {url}")
            logger.info(f"Request params: {params}")

            if method == "GET":
                response = requests.get(url, headers=headers, params=params)
            elif method == "POST":
                response = requests.post(url, headers=headers, params=params)
            else:
                raise ValueError("Unsupported HTTP method")

            logger.info(f"Response status: {response.status_code}")
            logger.info(f"Response body: {response.text}")

            if response.status_code != 200:
                logger.error(f"Error response: {response.text}")
                raise Exception(f"Binance API Error: {response.text}")

            return response.json()

        except requests.exceptions.RequestException as e:
            logger.error(f"HTTP Request failed: {str(e)}")
            raise

    # Public method to get account info
    def get_account_info(self):
        return self._send_request("GET", "/fapi/v2/account", {})