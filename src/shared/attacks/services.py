import re
import socket
from contextlib import contextmanager
from typing import Generator, Optional

from constants import IP_REGEX
from shared.attacks.models import AttackRequest, Target
from shared.errors import UserError


class BaseService:
    def __init__(self, attack_request: AttackRequest) -> None:
        self._attack_request = attack_request
        self._ping_fails = 0
        self.POSSIBLE_PING_FAILS = 1_000

    def _get_site_address(self) -> str:
        results = self._attack_request.target.address.split("/")
        return results[0]

    def get_socket(self, target: Target) -> Optional[socket.socket]:
        """Return socket instance if it is reachable"""
        try:
            if not re.match(IP_REGEX, target.address):
                address = self._get_site_address()
                ip_address = socket.gethostbyname(address)
            else:
                ip_address = target.address

            sock = socket.socket()
            sock.connect((ip_address, target.port))
            return sock
        except TimeoutError:
            return None
        except socket.error as err:
            raise UserError(str(err))

    @contextmanager
    def socket_connection(self, target: Target) -> Generator[Optional[socket.socket], None, None]:
        sock: Optional[socket.socket] = self.get_socket(target)
        try:
            yield sock
        finally:
            sock.close() if sock else None

    def ping(self, target: Target) -> Generator[bool, None, None]:
        """
        Use it with for loop.
        Returns `True` if target is reachable every 1_000 packets.
        raise StopIteration if not
        """
        while True:
            if self.get_socket(target):
                print(f"[+] Host {target.address} is reachable")
                yield True
                continue

            self._ping_fails += 1
            print(self._ping_fails, " Fails")
            if self._ping_fails > self.POSSIBLE_PING_FAILS:
                break
