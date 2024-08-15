# coding: utf-8


def format(open_port_list: list[int]) -> str:
    """

    Args:
        dict_result (dict[int, str])

    Returns:
        str: "port: status"
    """
    print("PORT       STATE SERVICE")
    for open_port in open_port_list:
        # open_port/tcpを10文字の幅で表示する。
        print(f"{open_port}/tcp".ljust(10), "open")
