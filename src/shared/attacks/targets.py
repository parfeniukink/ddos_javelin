from dataclasses import dataclass

from shared.collections import Model


@dataclass(frozen=True)
class Target(Model):
    ip: str
    port: int
