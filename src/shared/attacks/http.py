from dataclasses import dataclass

from shared.collections import Enum, Model


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
