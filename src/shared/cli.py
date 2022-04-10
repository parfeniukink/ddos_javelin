from dataclasses import dataclass
from typing import Optional

from packets.models import PacketSizes
from shared.attacks import AttackTypes, HttpMethods, HttpSchemas


@dataclass
class Cli:
    attack_type: AttackTypes
    address: str
    port: int
    size: Optional[PacketSizes]
    http_schema: Optional[HttpSchemas]
    http_method: Optional[HttpMethods]
    payload: Optional[dict]
    debug: bool


def get_dict_payload(obj: Cli, field: str, name: Optional[str] = None) -> dict:
    name = name if name else field
    value = getattr(obj, field)
    return {name: value} if value else {}
