# coding: utf-8
import sys
from scapy.all import IP, TCP, sr1, conf
from dataclasses import dataclass
from .Scan import Scan


@dataclass
class SynScan(Scan):
    def run(self) -> list[int]:
        """
        run SYN scan

        Returns:
            list[int]: open ports list
        """
        self.open_port_list = []

        conf.verb = 0  # packet送信時のログをSTDOUTに表示しない
        for port in self.target_port_list:
            # SYN packetを作成して送信する
            syn_packet = IP(dst=self.target_ip) / TCP(dport=port, flags="S")
            try:
                response_packet = sr1(syn_packet, timeout=self.max_rtt_timeout / 1000)
            except PermissionError:
                print(
                    "You requested a scan type which requires root privileges.\nQUITTING!"
                )
                sys.exit(1)

            try:
                response_packet.haslayer(TCP)
            except AttributeError:
                continue
            # SYN/ACKパケットが返ってきた際にopen portとしてリストに追加
            if response_packet[TCP].flags == "SA":
                self.open_port_list.append(port)

        return self.open_port_list
