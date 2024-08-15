# coding: utf-8
from dataclasses import dataclass
from abc import abstractmethod


@dataclass
class Scan:
    target_ip: str
    target_port_list: list[int]

    @abstractmethod
    def run(self) -> None:
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
