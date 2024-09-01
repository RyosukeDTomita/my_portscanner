# coding utf-8
import socket
import re
import sys
from .options import parse_args
from .get_datetime import get_datetime_now
from .scan_tools import ConnectScan
from .scan_tools import SynScan
from .scan_tools import UdpScan
from .version import __version__


def main():
    args = parse_args()

    print(
        f"Starting my_portscanner {__version__} ( https://github.com/RyosukeDTomita/my_portscanner ) at {get_datetime_now()}"
    )

    # localhostを指定したスキャンはコンテナ内のlocalhostを指すので無効にする。
    if (args["target_ip"] == "localhost") or (args["target_ip"] == "127.0.0.1"):
        print(
            "[WARNING]: When executed via `docker run`, scan targeting `localhost` is not valid.\nQUIITING!"
        )
        sys.exit(1)

    # target_ipがipアドレスの形式でない場合はhost名を名前解決する。
    match = re.match(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$", args["target_ip"])
    if not match:
        try:
            target_ip = socket.gethostbyname(args["target_ip"])
        except socket.gaierror:
            print(f'Failed to resolve "{args["target_ip"]}".')
    else:
        target_ip = args["target_ip"]
    print(f"my_portscanner scan report for {args["target_ip"]} ({target_ip})")

    if args["scan_type"] == "connect":
        scan = ConnectScan(
            target_ip=target_ip,
            target_port_list=args["port"],
            max_rtt_timeout=args["max_rtt_timeout"],
            max_parallelism=args["max_parallelism"],
            no_ping=args["no_ping"],
        )
    elif args["scan_type"] == "stealth":
        scan = SynScan(
            target_ip=target_ip,
            target_port_list=args["port"],
            max_rtt_timeout=args["max_rtt_timeout"],
            max_parallelism=args["max_parallelism"],
            no_ping=args["no_ping"],
        )
    elif args["scan_type"] == "udp":
        scan = UdpScan(
            target_ip=target_ip,
            target_port_list=args["port"],
            max_rtt_timeout=args["max_rtt_timeout"],
            max_parallelism=args["max_parallelism"],
            no_ping=args["no_ping"],
        )
    else:
        print("invalid scan type")
        sys.exit(1)

    if args["debug"]:
        print(scan)

    scan.run()
    scan.print_result()


__all__ = ["main"]
