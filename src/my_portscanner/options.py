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
    parser.add_argument("-oN", "--file_txt", help="output txt file name.", type=str)
    parser.add_argument(
        "-p",
        "--port",
        help="port number lists. port number range e.g: -p 22,80,443 -p 22-30",
        type=str,
    )
    parser.add_argument("--version", action="version", version=__version__)
    p = parser.parse_args()

    if "," in p.port:
        port_list = [int(x) for x in p.port.split(",")]
    elif "-" in p.port:
        port_list = [
            int(x)
            for x in range(int(p.port.split("-")[0]), int(p.port.split("-")[1]) + 1, 1)
        ]
    else:
        # default port list
        port_list = [22, 80, 443]

    if p.stealth_scan:
        scan_type = "stealth"
    else:
        scan_type = "connect"

    args = {
        "target_ip": p.target_ip,
        "file_txt": p.file_txt,
        "port": port_list,
        "scan_type": scan_type,
    }
    return args
