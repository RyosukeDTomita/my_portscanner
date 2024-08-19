# coding: utf-8
import socket
from dataclasses import dataclass
from .Scan import Scan


@dataclass
class ConnectScan(Scan):

    def run(self) -> list[int]:
        """_summary_
        run connect scan

        NOTE: https://docs.python.org/ja/3/library/socket.html#socket.socket.connect_ex によるとconnece_exは例外を送出せずにエラーコードを戻り値として返すため，例外処理をしない。
        Returns:
            list[int]: open ports list
        """
        self.open_port_list = []
        for port in self.target_port_list:
            s = socket.socket()

            error_code = s.connect_ex((self.target_ip, port))  #
            if error_code == 0:
                self.open_port_list.append(port)
            s.close()
        return self.open_port_list
