# coding: utf-8
import socket
import asyncio
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
        self.scan_result = asyncio.run(self._async_run())
        return self.scan_result

    def _port_scan(self, port: int) -> dict:
        s = socket.socket()
        s.settimeout(self.max_rtt_timeout / 1000)

        try:
            errno = s.connect_ex((self.target_ip, port))
        finally:
            s.close()

        if errno == 0:
            return {"port": port, "state": "open"}
        # NOTE: ConnectionRefusedErrorはerrnoが111
        elif errno == 111:
            return {"port": port, "state": "closed"}
        # NOTE: timeoutの場合はerrnoが11
        elif errno == 11:
            return {"port": port, "state": "filtered"}
        else:
            return {"port": port, "state": "unknown"}
