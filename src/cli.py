import argparse
from core import format_weather


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="weather-cli",
        description="Simple weather formatting CLI",
    )
    parser.add_argument(
        "city",
        help="City name",
    )
    parser.add_argument(
        "--temp",
        type=float,
        required=True,
        help="Temperature in Celsius",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    message = format_weather(args.city, args.temp)
    print(message)


if __name__ == "__main__":
    main()
