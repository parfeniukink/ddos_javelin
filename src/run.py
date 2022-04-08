from attacks import AttackHandler
from cli_parser import CliParser
from shared.attacks import AttackRequest, AttackTypes
from shared.attacks.http import HttpRequestMeta
from shared.attacks.targets import Target
from shared.cli import Cli, get_dict_payload


def main() -> None:
    parser = CliParser()
    parser.add_arguments()
    args: Cli = parser.validate_args()

    size_payload = get_dict_payload(args, "size")
    payload = get_dict_payload(args, "payload")
    if args.attack_type is not AttackTypes.HTTP:
        http_meta = HttpRequestMeta()
    else:
        http_schema_payload = get_dict_payload(args, "http_schema", "schema")
        http_method_payload = get_dict_payload(args, "http_method", "method")
        http_data = http_schema_payload | http_method_payload | payload
        http_meta = HttpRequestMeta(**http_data)

    attack_request: AttackRequest = AttackRequest(
        target=Target(address=args.address, port=args.port),
        attack_type=args.attack_type,
        http_meta=http_meta,
        **size_payload,
    )

    attack_handler: AttackHandler = AttackHandler(attack_request=attack_request)
    attack_handler.start()


if __name__ == "__main__":
    main()
