from typing import Optional, Union

from shared.attacks import AttackRequest
from shared.attacks.core import BaseService
from shared.randoms import Random


class HttpService(BaseService):
    def __init__(self, attack_request: AttackRequest) -> None:
        super().__init__()
        self._attack_request = attack_request
        self.__duplicates_headers_counter = 0
        self.__cached_headers: Optional[dict] = None
        self.__duplicates_http_payloads = 0
        self.__cached_http_payload: Optional[dict] = None

    @property
    def _random_headers(self) -> dict:
        return {
            "connection": "keep-alive",
            "pragma": "no-cache",
            "cache-control": "no-cache",
            "accept-encoding": "gzip, deflate, br",
            "user-agent": f"{Random.get_user_agent()}",
        }

    @property
    def http_headers(self) -> dict:
        self.__duplicates_headers_counter += 1

        if self.__duplicates_headers_counter % 500 == 0:
            self.__cached_headers = None

        if self.__cached_headers is None:
            self.__cached_headers = self._random_headers

        return self.__cached_headers

    def _get_http_payload(self, data: Optional[Union[dict, list]]) -> dict:
        if not data:
            return {Random.get_random_string(10): Random.get_random_string(20) for _ in range(10)}

        if isinstance(data, dict):
            return data

        return {field: Random.get_random_string(20) for field in data}

    def get_http_payload(self, data: Optional[Union[dict, list]]) -> dict:
        """Return random dict payload if received list of fields"""
        self.__duplicates_http_payloads += 1

        if self.__duplicates_http_payloads % 100 == 0:
            self.__cached_http_payload = None

        if self.__cached_http_payload is None:
            self.__cached_http_payload = self._get_http_payload(data)

        return self.__cached_http_payload
