# coding: utf-8
import socket
import re
from .options import parse_args
from .get_datetime import get_datetime_now
from .scan_tools import ConnectScan
from .version import __version__


def main():
    args = parse_args()

    print(
        f"Starting my_portscanner {__version__} ( https://github.com/RyosukeDTomita/my_portscanner ) at {get_datetime_now()}"
    )

    # target_ipがipアドレスの形式でない場合はhost名を名前解決する。
    match = re.match(
        r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$", args["target_ip"]
    )
    if not match:
        target_ip = socket.gethostbyname(args["target_ip"])
    else:
        target_ip = args["target_ip"]
    print(f"my_portscanner scan report for {args["target_ip"]} ({target_ip})")

    if args["connect_scan"]:
        print("connect scan")
        connect_scan = ConnectScan(target_ip=target_ip, target_port_list=args["port"])
        connect_scan.run()
        connect_scan.print_result()


__all__ = ["main"]
