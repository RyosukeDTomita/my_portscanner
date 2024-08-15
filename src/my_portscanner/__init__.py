# coding: utf-8
from .options import parse_args
from .toml_parser import get_project_version
from .get_datetime import get_datetime


def main():
    print(
        f"Starting my_portscanner {get_project_version()} ( https://github.com/RyosukeDTomita/my_portscanner ) at {get_datetime()}"
    )

    args = parse_args()
    print(args)
    if args.connect_scan:
        print("connect scan")


__all__ = ["main"]
