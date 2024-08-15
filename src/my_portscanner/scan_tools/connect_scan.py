# coding: utf-8
import socket


def run(target_ip: str, target_port_list: list[int]) -> list[int]:
    """_summary_

    Args:
        target_ip (str)
        target_ports (list[int])

    Returns:
        list[int]: open ports list
    """
    open_port_list = []
    for port in target_port_list:
        s = socket.socket()
        error_code = s.connect_ex((target_ip, port))
        if error_code == 0:
            open_port_list.append(port)
        s.close()
    return open_port_list
