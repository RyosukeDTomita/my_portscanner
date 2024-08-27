# coding: utf-8
from dataclasses import dataclass
from abc import abstractmethod


@dataclass
class Scan:
    target_ip: str
    target_port_list: list[int]
    max_rtt_timeout: int
    max_parallelism: int

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
    
    def __str__(self) -> str:
        """_summary_
        インスタンスの情報を文字列で返す
        """
        if self.target_port_list == list(range(0, 65536)):
            target_port_list_fmt = "all"
        else:
            target_port_list_fmt = self.target_port_list
        return f"Scan(target_ip={self.target_ip}, target_port_list={target_port_list_fmt}, scan_type={self.__class__.__name__}, max_rtt_timeout={self.max_rtt_timeout}, max_parallelism={self.max_parallelism})"

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
        # 出力が100行を超えそうなときは，closed portsを非表示にする。
        if len(self.scan_result) > 100:
            self.scan_result = [
                port_info for port_info in self.scan_result if port_info["state"] != "closed"
            ]
        # port6桁+/tcpで10桁
        print(f"{"PORT":<10} {"STATE":<8} SERVICE")
        for port_info in self.scan_result:
            print(
                f"{port_info["port"]}/tcp".ljust(10)
                + " "
                + f"{port_info["state"]:<8} unknown"
            )
