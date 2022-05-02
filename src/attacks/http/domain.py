from enum import auto

from shared.collections import Enum


class DDoSSecurities(Enum):
    DDOS_GUARD = auto()
    CLOUDFLARE = auto()
