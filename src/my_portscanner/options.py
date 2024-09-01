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
    parser.add_argument("target_ip", help="set target IP address or FQDN.", type=str)
    parser.add_argument(
        "-sT",
        "--connect_scan",
        action="store_true",
        help="TCP connect scan (default)",
    )
    parser.add_argument(
        "-sS",
        "--stealth_scan",
        action="store_true",
        help="TCP SYN scan",
    )
    parser.add_argument(
        "-sU",
        "--udp_scan",
        action="store_true",
        help="UDP scan",
    )
    parser.add_argument(
        "-p",
        "--port",
        default="22,80,443",
        help="port number, port number lists, port number range. e.g: -p 22 -p 22,80,443 -p 22-30 -p- (all port)",
        type=str,
    )
    parser.add_argument(
        "--max-rtt-timeout",
        default=1000,
        help="set max rtt timeout (ms). default=1000",
        type=int,
    )
    parser.add_argument(
        "--version",
        action="version",
        help="display my_portscanner version and exit",
        version=__version__,
    )
    parser.add_argument(
        "--max-parallelism", default=None, help="set max parallelism ", type=int
    )
    parser.add_argument(
        "-d",
        "--debug",
        action="store_true",
        help="display debug info",
    )
    parser.add_argument(
        "-Pn",
        "--no-ping",
        action="store_true",
        help="no ping sent before scanning",
    )
    p = parser.parse_args()

    try:
        scan_type = _select_scan_type(p.connect_scan, p.stealth_scan, p.udp_scan)
    except ValueError as e:
        print(e)
        sys.exit(1)

    try:
        if scan_type == "udp":
            port_list = _create_port_list(p.port, is_udp=True)
        else:
            port_list = _create_port_list(p.port)
    except ValueError as e:
        print(e)
        sys.exit(1)

    args = {
        "target_ip": p.target_ip,
        "port": port_list,
        "scan_type": scan_type,
        "max_rtt_timeout": p.max_rtt_timeout,
        "max_parallelism": p.max_parallelism,
        "debug": p.debug,
        "no_ping": p.no_ping,
    }
    return args


def _create_port_list(port: Union[str, None], is_udp=False) -> list[int]:
    """_create_port_list.
    -p オプションの引数をリストに変換する

    Args:
        port str: port number lists. port number range e.g: -p 22,80,443 -p 22-30
        port None: no -p option

    Returns:
        list[int]: port_list
    """
    if port.isdigit():
        return [int(port)]
    # all port
    if port == "-":
        if is_udp:
            return list(range(1, 1024))
        return list(range(0, 65536))

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


def _select_scan_type(connect_scan: bool, stealth_scan: bool, udp_scan: bool) -> str:
    """_summary_
    複数のオプションが同時に指定されないようにしつつ，適切なスキャンタイプを返す
    Args:
        connect_scan: bool
        stealth_scan: bool
        udp_scan: bool

    Returns:
        str: scan_type
    """
    # 複数のオプションが指定されていたらエラー
    options_count = sum([connect_scan, stealth_scan, udp_scan])
    if options_count > 1:
        raise ValueError("[-sT] [-sS] [-sU] options are exclusive.")

    # default options
    if options_count == 0:
        return "connect"

    if stealth_scan:
        return "stealth"
    elif udp_scan:
        return "udp"
    else:
        return "connect"
