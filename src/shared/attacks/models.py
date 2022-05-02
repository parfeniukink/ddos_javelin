from dataclasses import dataclass
from typing import Optional, Protocol

from packets.models import PacketSizes
from shared.collections import Enum, Model


@dataclass(frozen=True)
class Target(Model):
    address: str
    port: int


##########################################
# HTTP
##########################################
class HttpSchemas(Enum):
    HTTP = "http"
    HTTPS = "https"


class HttpMethods(Enum):
    GET = "GET"
    POST = "POST"
    HEAD = "HEAD"


@dataclass(frozen=True)
class HttpRequestMeta(Model):
    schema: HttpSchemas = HttpSchemas.HTTPS
    method: HttpMethods = HttpMethods.GET
    path: str = "/"


##########################################
# ATTACK CONFIGURATION
##########################################


class AttackTypes(Enum):
    HTTP = "HTTP"
    SYN_FLOOD = "SYN_FLOOD"


@dataclass(frozen=True)
class AttackRequest(Model):
    target: Target
    size: PacketSizes = PacketSizes.MEDIUM
    attack_type: AttackTypes = AttackTypes.HTTP
    http_meta: Optional[HttpRequestMeta] = None
    payload: Optional[dict] = None


class Attack(Protocol):
    def __init__(self, attack_request: AttackRequest) -> None:
        ...

    def run(self) -> None:
        """Run attack"""
        ...

    def run_debug(self) -> None:
        """Run attack in debug mode"""
        ...
