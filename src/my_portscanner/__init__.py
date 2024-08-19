# coding utf-8
import socket
import re
from .options import parse_args
from .get_datetime import get_datetime_now
from .scan_tools import ConnectScan
from .scan_tools import SynScan
from .version import __version__


def main():
    args = parse_args()

    print(
        f"Starting my_portscanner {__version__} ( https://github.com/RyosukeDTomita/my_portscanner ) at {get_datetime_now()}"
    )

    # localhostを指定したスキャンはコンテナ内のlocalhostを指すので無効にする。
    if ((args["target_ip"] == "localhost") or (args["target_ip"] == "127.0.0.1")):
        print("[WARNING]: When executed via `docker run`, scan targeting `localhost` is not valid.")

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
        print("connect scan")
        connect_scan = ConnectScan(target_ip=target_ip, target_port_list=args["port"])
        connect_scan.run()
        connect_scan.print_result()
    elif args["scan_type"] == "stealth":
        print("stealth scan")
        syn_scan = SynScan(target_ip=target_ip, target_port_list=args["port"])
        syn_scan.run()
        syn_scan.print_result()
    else:
        print("invalid scan type")
        exit()


__all__ = ["main"]
