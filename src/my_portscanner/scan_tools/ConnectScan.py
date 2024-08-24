# coding: utf-8
import socket
from dataclasses import dataclass
from .Scan import Scan


@dataclass
class ConnectScan(Scan):
    def run(self) -> list[dict]:
        """_summary_
        run connect scan

        NOTE: https://docs.python.org/ja/3/library/socket.html#socket.socket.connect_ex によるとconnece_exは例外を送出せずにエラーコードを戻り値として返すため，例外処理をしない。
        Returns:
            scan_result: list[dict]
            e.g: [{"port": port, "state": "open"}, "port": port, "state": "closed"} ...]
        """
        self.scan_result = []
        for port in self.target_port_list:
            s = socket.socket()
            s.settimeout(self.max_rtt_timeout / 1000)

            errno = s.connect_ex((self.target_ip, port))  #
            if errno == 0:
                self.scan_result.append({"port": port, "state": "open"})
            # NOTE: ConnectionRefusedErrorはerrnoが111
            elif errno == 111:
                self.scan_result.append({"port": port, "state": "closed"})
            # NOTE: timeoutの場合はerrnoが11
            elif errno == 11:
                self.scan_result.append({"port": port, "state": "filtered"})
            else:
                print(f"errno: {errno}")  # FIXME
            s.close()
        return self.scan_result
