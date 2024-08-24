# coding: utf-8
import sys
from scapy.all import IP, TCP, sr1, conf
from dataclasses import dataclass
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
        self.scan_result = []

        conf.verb = 0  # packet送信時のログをSTDOUTに表示しない
        for port in self.target_port_list:
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
                self.scan_result.append({"port": port, "state": "filtered"})
                continue

            try:
                response_packet.haslayer(TCP)
            except AttributeError:
                continue
            # SYN/ACKパケットが返ってきた際にopen portとしてリストに追加
            if response_packet[TCP].flags == "SA":
                self.scan_result.append({"port": port, "state": "open"})
            # closed portの場合はRSTパケットが返ってくる
            elif response_packet[TCP].flags == "RA":
                self.scan_result.append({"port": port, "state": "closed"})

        return self.scan_result
