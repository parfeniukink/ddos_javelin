from dataclasses import dataclass
from enum import Enum as _Enum
from enum import IntEnum as _IntEnum
from enum import unique
from typing import Generator, Iterable


class EnumMixin:
    @classmethod
    def values(cls: Iterable) -> Generator:
        return (i.value for i in cls)


@unique
class Enum(_Enum):
    pass


@unique
class IntEnum(_IntEnum):
    pass


@dataclass(frozen=True)
class Model:
    """Use it only for inheritance in other dataclasses"""

    def values(self) -> Generator:
        return (getattr(self, field, None) for field in self.__dataclass_fields__)
