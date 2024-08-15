# coding: utf-8
import socket
import re
from .options import parse_args
from .toml_parser import get_project_version
from .get_datetime import get_datetime_now


def main():
    print(
        f"Starting my_portscanner {get_project_version()} ( https://github.com/RyosukeDTomita/my_portscanner ) at {get_datetime_now()}"
    )

    args = parse_args()
    print(args)

    if args["connect_scan"]:
        print("connect scan")

    # target_ipがipアドレスの形式でない場合はhost名を名前解決する。
    match = re.match(
        r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$", args["target_ip"]
    )
    if not match:
        target_ip = socket.gethostbyname(args["target_ip"])
    else:
        target_ip = args["target_ip"]
    print(f"target_ip: {target_ip}")
    
    print(f"my_portscanner scan report for {args["target_ip"]} ({target_ip})")


__all__ = ["main"]
