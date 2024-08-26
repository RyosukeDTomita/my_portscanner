# coding: utf-8
import sys
from scapy.all import IP, TCP, sr1, conf
from dataclasses import dataclass
import asyncio
from .Scan import Scan


@dataclass
class SynScan(Scan):
    def run(self) -> list[dict]:
        """
        run SYN scan

        Returns:
            scan_result: list[dict]
            e.g: [{"port": port, "state": "open"}, "port": port, "state": "closed"} ...]
        """
        self.scan_result = asyncio.run(self._async_run())
        return self.scan_result

    async def _async_run(self):
        scan_result = []
        for i in range(self.target_port_list[0], self.target_port_list[-1], 4):
            results = await asyncio.gather(
                self._create_task(self.target_port_list[i]),
                self._create_task(self.target_port_list[i + 1]),
                self._create_task(self.target_port_list[i + 2]),
                self._create_task(self.target_port_list[i + 3]),
            )
            for result in results:
                scan_result.append(result)
        return scan_result

    async def _create_task(self, port: int):
        loop = asyncio.get_event_loop()
        scan_result = await loop.run_in_executor(None, self._port_scan, port)
        return scan_result

    def _port_scan(self, port: int) -> list[dict]:
        """
        run SYN scan with asyncio

        Returns:
            scan_result: list[dict]
            e.g: [{"port": port, "state": "open"}, "port": port, "state": "closed"} ...]
        """
        conf.verb = 0  # packet送信時のログをSTDOUTに表示しない
        syn_packet = IP(dst=self.target_ip) / TCP(dport=port, flags="S")
        try:
            response_packet = sr1(syn_packet, timeout=self.max_rtt_timeout / 1000)
        except PermissionError:
            print(
                "You requested a scan type which requires root privileges.\nQUITTING!"
            )
            sys.exit(1)

        # FWなどによってパケットがフィルタリングされた場合にはレスポンスなし
        if response_packet is None:
            return {"port": port, "state": "filtered"}

        try:
            response_packet.haslayer(TCP)
        except AttributeError:
            # SYN/ACKパケットが返ってきた際にopen portとしてリストに追加
            pass
        if response_packet[TCP].flags == "SA":
            return {"port": port, "state": "open"}
        # closed portの場合はRSTパケットが返ってくる
        elif response_packet[TCP].flags == "RA":
            return {"port": port, "state": "closed"}
        else:
            return {"port": port, "state": "unknown"}
