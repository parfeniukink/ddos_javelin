from typing import Optional

from shared.attacks import AttackRequest, BaseService
from shared.randoms import Random


class HttpService(BaseService):
    def __init__(self, attack_request: AttackRequest) -> None:
        super().__init__(attack_request=attack_request)
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

    def get_http_payload(self, data: Optional[dict]) -> dict:
        """Return random dict payload if received list of fields"""
        self.__duplicates_http_payloads += 1

        if self.__duplicates_http_payloads % 100 == 0:
            self.__cached_http_payload = None

        if self.__cached_http_payload is None:
            self.__cached_http_payload = super().get_data_payload(data)

        return self.__cached_http_payload
