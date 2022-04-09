from dataclasses import dataclass
from enum import Enum as _Enum
from enum import IntEnum as _IntEnum
from enum import unique
from typing import Generator, Iterable


@unique
class Enum(_Enum):
    @classmethod
    def values(cls: Iterable) -> list:
        return [i.value for i in cls]


@unique
class IntEnum(_IntEnum):
    @classmethod
    def values(cls: Iterable) -> list:
        return [i.value for i in cls]

    @classmethod
    def names(cls: Iterable) -> list:
        return [i.name for i in cls]


@dataclass(frozen=True)
class Model:
    """Use it only for inheritance in other dataclasses"""

    def values(self) -> Generator:
        return (getattr(self, field, None) for field in self.__dataclass_fields__)
