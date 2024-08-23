# coding: utf-8
import argparse
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

    port_list = _create_port_list(p.port)

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


def _create_port_list(port: str) -> list[int]:
    """_create_port_list.
    -p オプションの引数をリストに変換する

    Args:
        port (str): port number lists. port number range e.g: -p 22,80,443 -p 22-30

    Returns:
        list[int]: e.g: [22, 80, 443]
    """
    if "," in port:
        port_list = [int(x) for x in port.split(",")]
    elif "-" in port:
        port_list = [
            int(x)
            for x in range(int(port.split("-")[0]), int(port.split("-")[1]) + 1, 1)
        ]
    else:
        # default port list
        port_list = [22, 80, 443]
    return port_list
