import random
import string
from typing import Optional

from constants import REFERERS_FILENAME, USER_AGENTS_FILENAME
from shared.files import get_file_lines


class Random:
    referers = get_file_lines(REFERERS_FILENAME)
    user_agents = get_file_lines(USER_AGENTS_FILENAME)
    cached_byte_payload: Optional[bytes] = None

    @staticmethod
    def get_ip() -> str:
        ip = []
        for _ in range(0, 4):
            ip.append(str(random.randint(1, 255)))

        return ".".join(ip)

    @classmethod
    def get_referrer(cls) -> str:
        return random.choice(cls.referers)

    @classmethod
    def get_user_agent(cls) -> str:
        return random.choice(cls.user_agents)

    @classmethod
    def get_bytes(cls, n: int = 0) -> bytes:
        if cls.cached_byte_payload:
            return cls.cached_byte_payload

        if n < 1:
            raise ValueError("`n` must be more than 1")

        return b"\x00" * n

    @classmethod
    def get_random_string(cls, n: int = 100) -> str:
        return "".join((random.choice(string.ascii_letters) for _ in range(n)))
