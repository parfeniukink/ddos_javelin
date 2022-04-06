import socket
from dataclasses import dataclass
from typing import Protocol, Union

from packets.models import PacketSizes
from shared.attacks.http import HttpAddress
from shared.attacks.targets import Target
from shared.collections import Enum, Model


class AttackTypes(Enum):
    HTTP = "HTTP"


@dataclass(frozen=True)
class AttackRequest(Model):
    address: Union[HttpAddress, Target]
    size: PacketSizes
    attack_type: AttackTypes


class Attack(Protocol):
    def __init__(self, attack_request: AttackRequest) -> None:
        ...

    def run(self) -> None:
        """Create and return packet to send"""
        ...


class BaseService:
    def __init__(self) -> None:
        self._counter = 0
        self._fails = 0

    def get_socket(self, target: Target) -> socket.socket:
        sock = socket.socket()
        sock.connect(tuple(target.values()))

        return sock

    def ping(self, sock: socket.socket) -> bool:
        """
        Returns False if amount of fails is more than 1_000
        Check every 10_000 tries.

        NOTE: Use only for while loops
        """
        self._counter += 1

        if self._counter % 10_000 == 0:
            self._counter = 0
            self._fails += 1 if sock.recv(1) else 0

        if self._counter % 1_000 == 0:
            self._fails += 1 if sock.recv(1) else 0
            if self._fails > 1_000:
                return False

        return True
