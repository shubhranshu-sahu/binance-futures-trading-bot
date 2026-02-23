import os
import time
import hmac
import hashlib
from urllib import response
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
        url = f"{self.base_url}{endpoint}"

        params["timestamp"] = self._get_timestamp()
        query_string = urlencode(params)
        signature = self._sign(query_string)
        params["signature"] = signature

        headers = {
            "X-MBX-APIKEY": self.api_key
        }

        # Mask signature in logs
        safe_params = params.copy()
        safe_params.pop("signature", None)

        max_retries = 3
        backoff_factor = 2

        for attempt in range(1, max_retries + 1):
            try:
                logger.info(f"Sending {method} request to {url}")
                logger.info(f"Request params: {safe_params}")

                if method == "GET":
                    response = requests.get(
                        url,
                        headers=headers,
                        params=params,
                        timeout=10
                    )
                elif method == "POST":
                    response = requests.post(
                        url,
                        headers=headers,
                        params=params,
                        timeout=10
                    )
                else:
                    raise ValueError("Unsupported HTTP method")

                logger.info(f"Response status: {response.status_code}")

                # Retry only on server errors (5xx)
                if response.status_code >= 500:
                    raise requests.exceptions.RequestException(
                        f"Server error: {response.status_code}"
                    )

                # Handle client errors (4xx) without retry
                if response.status_code >= 400:
                    logger.error(f"API Error: {response.text}")
                    raise Exception(f"Binance API Error: {response.text}")

                return response.json()

            except requests.exceptions.RequestException as e:
                logger.warning(f"Attempt {attempt} failed: {str(e)}")

                if attempt == max_retries:
                    logger.error("Max retries reached. Request failed.")
                    raise Exception("Network error after multiple retries.")

                sleep_time = backoff_factor ** attempt
                logger.info(f"Retrying in {sleep_time} seconds...")
                time.sleep(sleep_time)


    # Public method to get account info
    def get_account_info(self):
        return self._send_request("GET", "/fapi/v2/account", {})