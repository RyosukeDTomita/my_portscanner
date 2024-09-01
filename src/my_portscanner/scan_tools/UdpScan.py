# coding: utf-8
from scapy.all import UDP, IP, sr1, ICMP, conf
import asyncio
from .Scan import Scan


class UdpScan(Scan):
    def run(self) -> list[dict]:
        """
        Run UDP scan
        Returns:
            scan_result: list[dict]
            e.g: [{"port": port, "state": "open"}, {"port": port, "state": "closed"}, ...]
        """
        if not self.no_ping:
            self._get_latency()
        self.scan_result = asyncio.run(self._async_run())
        # NOTE: 非同期処理により複数回PermissoinErrorが上がらないようにするため，例外の伝播を行っている。
        return self.scan_result

    def _port_scan(self, port: int) -> dict:
        """
        Run UDP scan for a single port
        非同期処理で実行される関数
        Args:
            port int: port_number
        Returns:
            dict: {"port": port, "state": state}
        """
        conf.verb = 0  # packet送信時のログをSTDOUTに表示しない
        udp_packet = IP(dst=self.target_ip) / UDP(dport=port)

        response = sr1(udp_packet, timeout=self.max_rtt_timeout / 1000)

        # timeoutしてresponseなしの場合はportが開いているのかFWによってICMPメッセージがフィルタリングされているかの判断ができないため，open|filteredとする。
        if response is None:
            return {"port": port, "state": "open|filtered"}
        elif (
            (response.haslayer(ICMP))
            and (response.getlayer(ICMP).type == 3)
            and (response.getlayer(ICMP).code == 3)
        ):
            return {"port": port, "state": "closed"}
        else:
            return {"port": port, "state": "unknown"}
