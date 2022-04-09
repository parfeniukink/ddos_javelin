import re

from constants import IP_REGEX


def is_ip(value: str) -> bool:
    return bool(re.match(IP_REGEX, value))
