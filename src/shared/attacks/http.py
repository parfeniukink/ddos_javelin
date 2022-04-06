from dataclasses import dataclass

from shared.attacks.targets import Target
from shared.collections import Enum, Model


class HTTPSchemas(Enum):
    HTTP = "http"
    HTTPS = "https"


class HTTPMethods(Enum):
    GET = "GET"
    POST = "POST"


@dataclass(frozen=True)
class HttpAddress(Model):
    target: Target
    schema: str = HTTPSchemas.HTTPS.value
    path: str = "/"
