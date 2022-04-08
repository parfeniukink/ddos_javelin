from multiprocessing import Process, cpu_count

from attacks.http import HttpAttack
from shared.attacks import Attack, AttackRequest, AttackTypes


class AttackHandler:
    def __init__(self, attack_request: AttackRequest, *_, **__) -> None:
        self.cpu_count: int = cpu_count()
        self._attack: Attack = self._get_attack(attack_request)

    def _get_attack(self, attack_request: AttackRequest) -> Attack:
        if attack_request.attack_type == AttackTypes.HTTP:
            return HttpAttack(attack_request)
        return HttpAttack(attack_request)

    def start(self) -> None:
        print("[+] Attack started")
        pool = []
        for _ in range(self.cpu_count):
            p = Process(target=self._attack.run)
            pool.append(p)
            p.start()
        for p in pool:
            p.join()
        print("[+] Attack is done")

    # NOTE: Debugging
    # def start(self) -> None:
    #     self._attack.run()
    #     print("[+] Attack is done")
