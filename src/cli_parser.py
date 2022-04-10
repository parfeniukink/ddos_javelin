import argparse
import json
import re
from typing import Optional

from constants import (
    ADDRESS_REGEX,
    ARGPARSER_WELCOME_MESSAGE,
    MAX_PORT_NUMBER,
    MIN_PORT_NUMBER,
)
from packets.models import PacketSizes
from shared.attacks import AttackTypes, HttpMethods, HttpSchemas
from shared.cli import Cli


class CliParser:
    def __init__(self) -> None:
        self.parser = argparse.ArgumentParser(description=ARGPARSER_WELCOME_MESSAGE)
        self._attack_types = AttackTypes.values()
        self._packet_sizes = PacketSizes.names()
        self._http_schemas = HttpSchemas.values()
        self._http_methods = HttpMethods.values()

    def add_arguments(self) -> None:
        ENUM_DIVIDER = " | "

        attack_types = ENUM_DIVIDER.join(self._attack_types)
        self.parser.add_argument(
            "--attack",
            "--attack_type",
            dest="attack_type",
            required=True,
            help=f"Attack type. Allowed values {attack_types}",
        )

        self.parser.add_argument(
            "-a",
            "--address",
            dest="address",
            required=True,
            help="Examples: google.com | 192.168.1.2",
        )
        self.parser.add_argument(
            "-p",
            "--port",
            dest="port",
            required=True,
            help="Examples: 443 | 8000 | 80",
        )

        packet_sizes = ENUM_DIVIDER.join(self._packet_sizes)
        self.parser.add_argument(
            "-s",
            "--size",
            dest="size",
            help=f"The size of requested package. Allowed values: {packet_sizes}",
        )

        http_schemas = ENUM_DIVIDER.join(self._http_schemas)
        self.parser.add_argument(
            "--hs",
            "--http_schema",
            dest="http_schema",
            help=f"HTTP schema. Allowed values: {http_schemas}. Default HTTPS",
        )

        http_methods = ENUM_DIVIDER.join(self._http_methods)
        self.parser.add_argument(
            "--hm",
            "--http_method",
            dest="http_method",
            help=f"HTTP method. Allowed values: {http_methods}. Default GET",
        )

        self.parser.add_argument(
            "--pl",
            "--payload",
            dest="payload",
            help=(
                "Custom payload. If not selected use randomly-generated. "
                "Allowed type is python dictionary. "
                """Example: '{"username": "admin", "pass": "admin"}'"""
            ),
        )

        self.parser.add_argument(
            "--debug",
            dest="debug",
            action="store_true",
            default=False,
            help=(
                "Set this flag if you develop something."
                "It will reduce the amount of used CPUs to 1 and also it will not create any threads"
            ),
        )

    def _validate_attack_type(self) -> AttackTypes:
        value = self.args.attack_type.upper()
        if value not in self._attack_types:
            raise ValueError(f"Not allowed attack type - {self.args.attack_type}")

        return getattr(AttackTypes, value)

    def _validate_address(self) -> str:
        value = self.args.address
        if not re.match(ADDRESS_REGEX, value):
            raise ValueError(f"Not allowed attack type - {self.args.attack_type}")

        return value

    def _validate_port(self) -> int:
        try:
            port: int = int(self.args.port)
        except ValueError:
            raise ValueError("Port should be a number")
        if MIN_PORT_NUMBER > port > MAX_PORT_NUMBER:
            raise ValueError(f"You can use port in range between {MIN_PORT_NUMBER} and {MAX_PORT_NUMBER}")
        return port

    def _validate_size(self) -> Optional[PacketSizes]:
        if not self.args.size:
            return None

        value = self.args.size.upper()
        if value not in self._packet_sizes:
            raise ValueError(f"Not allowed packet size - {self.args.size}")

        return getattr(PacketSizes, value)

    def _validate_http_schema(self) -> Optional[HttpSchemas]:
        if not self.args.http_schema:
            return None

        value = self.args.http_schema
        if value not in self._http_schemas:
            raise ValueError(f"Not allowed HTTP schema - {value}")

        return getattr(HttpSchemas, value.upper())

    def _validate_http_method(self) -> Optional[HttpMethods]:
        if not self.args.http_method:
            return None

        value = self.args.http_method.upper()
        if value not in self._http_methods:
            raise ValueError(f"Not allowed HTTP method - {self.args.http_method}")

        return getattr(HttpMethods, value)

    def _validate_payload(self) -> Optional[dict]:
        if not self.args.payload:
            return None
        try:
            return json.loads(self.args.payload)
        except json.JSONDecodeError:
            raise ValueError("Can not parse payload data. It shoulf be dict")

    def validate_args(self) -> Cli:
        self.args: argparse.Namespace = self.parser.parse_args()

        return Cli(
            attack_type=self._validate_attack_type(),
            address=self._validate_address(),
            port=self._validate_port(),
            size=self._validate_size(),
            http_schema=self._validate_http_schema(),
            http_method=self._validate_http_method(),
            payload=self._validate_payload(),
            debug=self.args.debug,
        )
