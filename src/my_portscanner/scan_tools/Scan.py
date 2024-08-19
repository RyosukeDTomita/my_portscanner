# coding: utf-8
from dataclasses import dataclass
from abc import abstractmethod


@dataclass
class Scan:
    target_ip: str
    target_port_list: list[int]

    def __init__(self, *args, **kwargs):
        """_summary_

        継承専用のクラスのため，直接インスタンス化できないようにする。
        Raises:
            TypeError: _description_
        """
        if type(self) is Scan:
            raise TypeError(
                "Scan is an abstract class and cannot be instantiated directly"
            )

    @abstractmethod
    def run(self) -> list[int]:
        """_summary_
        port scanを実行するabstract method
        """
        pass

    def print_result(self) -> None:
        """
        port scanの結果を表示する
        """
        # port6桁+/tcpで10桁
        print(f"{"PORT":<10} STATE SERVICE")
        for open_port in self.open_port_list:
            # FIXME: open close以外のステータスを判別できるようになったら直す。
            print(f"{open_port}/tcp".ljust(10) + " " + f"{'open':<5} unknown")
