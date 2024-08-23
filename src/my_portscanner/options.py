# coding: utf-8
import argparse
import sys
from typing import Union
from .version import __version__


def parse_args() -> dict:
    """parse_args.
    実行時の引数をパースする

    Returns:
        dict:
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("target_ip", help="set target ip address.", type=str)
    parser.add_argument(
        "-sT",
        "--connect_scan",
        action="store_true",
        help="TCP connect scan",
    )
    parser.add_argument(
        "-sS",
        "--stealth_scan",
        action="store_true",
        help="TCP SYN scan",
    )
    parser.add_argument(
        "-p",
        "--port",
        help="port number lists. port number range e.g: -p 22,80,443 -p 22-30",
        type=str,
    )
    parser.add_argument("--max-rtt-timeout", help="set max rtt timeout (ms).", type=int)
    parser.add_argument("--version", action="version", version=__version__)
    p = parser.parse_args()

    try:
        port_list = _create_port_list(p.port)
    except ValueError as e:
        print(e)
        sys.exit(1)

    if p.stealth_scan:
        scan_type = "stealth"
    else:
        scan_type = "connect"

    if p.max_rtt_timeout is None:
        max_rtt_timeout = 1000  # ms
    else:
        max_rtt_timeout = p.max_rtt_timeout

    args = {
        "target_ip": p.target_ip,
        "port": port_list,
        "scan_type": scan_type,
        "max_rtt_timeout": max_rtt_timeout,
    }
    return args


def _create_port_list(port: Union[str, None]) -> list[int]:
    """_create_port_list.
    -p オプションの引数をリストに変換する

    Args:
        port str: port number lists. port number range e.g: -p 22,80,443 -p 22-30
        port None: no -p option

    Returns:
        list[int]: e.g: [22, 80, 443]
    """
    default_port_list = [22, 80, 443]

    if port is None:
        return default_port_list
    if port.isdigit():
        return [int(port)]

    # ,区切りをリストに変換
    if "," in port:
        port_list = [int(x) for x in port.split(",") if x.isdigit()]
        if port_list == []:
            raise ValueError("[-p] port list includes non-digit")
    # -のport範囲指定をリストに変換
    elif "-" in port:
        port_start_str, port_end_str = port.split("-")
        if (not port_start_str.isdigit()) or (not port_end_str.isdigit()):
            raise ValueError("[-p] port range includes non-digit")
        if int(port_start_str) > int(port_end_str):
            raise ValueError("[-p] port range start is larger than end")
        port_list = [int(x) for x in range(int(port_start_str), int(port_end_str) + 1)]
    return port_list
