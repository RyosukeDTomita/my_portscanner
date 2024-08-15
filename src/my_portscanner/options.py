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
        "-sT", "--connect_scan", default=True, help="TCP connect Scan", type=bool
    )
    parser.add_argument("-oN", "--file_txt", help="output txt file name.", type=str)
    parser.add_argument("-p", "--port", help="port number lists", type=str)
    parser.add_argument("-v", "--version", action="version", version=__version__)
    p = parser.parse_args()

    # 引数のport番号をint型のリストに変換する。
    if p.port is not None:
        port_list = [int(x) for x in p.port.split(",")]
    else:
        # default port list
        port_list = [22, 80, 443, 8080]

    args = {
        "target_ip": p.target_ip,
        "file_txt": p.file_txt,
        "port": port_list,
        "connect_scan": p.connect_scan,
    }
    return args
