# coding: utf-8
from scapy.all import IP, TCP, sr1, conf
import asyncio
import sys
from .Scan import Scan


class SynScan(Scan):
    def run(self) -> list[dict]:
        """
        Run SYN scan
        Returns:
            scan_result: list[dict]
            e.g: [{"port": port, "state": "open"}, {"port": port, "state": "closed"}, ...]
        """
        try:
            self.scan_result = asyncio.run(self._async_run())
        # NOTE: 非同期処理により複数回PermissoinErrorが上がらないようにするため，例外の伝播を行っている。
        except PermissionError:
            print(
                "You requested a scan type which requires root privileges.\nQUITTING!"
            )
            sys.exit(1)
        return self.scan_result

    def _port_scan(self, port: int) -> dict:
        """
        Run SYN scan for a single port
        非同期処理で実行される関数
        Args:
            port int: port_number
        Returns:
            dict: {"port": port, "state": state}
        """
        conf.verb = 0  # packet送信時のログをSTDOUTに表示しない
        syn_packet = IP(dst=self.target_ip) / TCP(dport=port, flags="S")

        try:
            # SYNパケットの作成する。パケットの生成には管理者権限が必要
            response_packet = sr1(syn_packet, timeout=self.max_rtt_timeout / 1000)
        except PermissionError:
            raise PermissionError

        # timeoutしてレスポンスなしの場合にはFW等によってパケットがフィルタリングされたと判断し，filterdにする。
        if response_packet is None:
            return {"port": port, "state": "filtered"}

        # TCPパケットでない場合には，Noneを返す。基本的には無い想定。
        try:
            response_packet.haslayer(TCP)
        except AttributeError:
            return

        # SYN/ACKパケットが返ってきた場合には，openとする
        if response_packet[TCP].flags == "SA":
            # RSTパケットを送信することで，コネクションを切断し，ハーフオープン状態を解消する
            sr1(
                IP(dst=self.target_ip) / TCP(dport=port, flags="RA"),
                timeout=self.max_rtt_timeout / 1000,
            )
            return {"port": port, "state": "open"}
        # RSTパケットが変えてきたときにはclosedとする
        elif response_packet[TCP].flags == "RA":
            return {"port": port, "state": "closed"}
        else:
            return {"port": port, "state": "unknown"}
