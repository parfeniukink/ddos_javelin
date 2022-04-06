import random

from constants import REFERERS_FILENAME, USER_AGENTS_FILENAME
from shared.files import get_file_lines


class Random:
    referers = get_file_lines(REFERERS_FILENAME)
    user_agents = get_file_lines(USER_AGENTS_FILENAME)

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
