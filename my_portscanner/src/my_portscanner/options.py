# coding: utf-8
import argparse


def parse_args() -> dict:
    """parse_args.
    Args:

    Returns:
        dict:
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("target_ip", help="set target ip address.", type=str)
    parser.add_argument("-oN", "--file_txt", help="output txt file name.", type=str)
    parser.add_argument("-p", "--port", help="port number lists", type=str)
    p = parser.parse_args()
    port_list_str = p.port.split(",")
    port_list = [int(x) for x in port_list_str]
    args = {"target_ip": p.target_ip, "file_txt": p.file_txt, "port": port_list}
    return args
