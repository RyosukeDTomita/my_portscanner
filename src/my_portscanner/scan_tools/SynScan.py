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
        Run SYN scan
        run()がsuper class Scanから継承した_async_run()を呼び出し，_create_task()で_port_scan()を非同期処理する。
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

    async def _async_run(self) -> list[dict]:
        """_summary_
        NOTE: 非同期処理を扱う関数を仕様するために，自身を非同期関数に変更して切り出している。
        Returns:
            scan_result: list[dict]
            e.g: [{"port": port, "state": "open"}, {"port": port, "state": "closed"}, ...]
            NOTE: `await asyncio.gather()`の戻り値の型は'_GatheringFuture'なので，list()でリストに変換している。
        """
        if self.max_parallelism is None:
            tasks = [self._create_task(port) for port in self.target_port_list]
        else:
            semaphore = asyncio.Semaphore(self.max_parallelism)  # 同時実行数を制限
            tasks = [
                self._create_task_with_semaphore(port, semaphore)
                for port in self.target_port_list
            ]
        return list(await asyncio.gather(*tasks))

    async def _create_task(self, port: int) -> dict:
        """_summary_
        _port_scanを非同期処理にするためのラッパー関数(no semaphore)
        Args:
            port int: port_number
        Returns:
            dict: {"port": port, "state": state}
        """
        # NOTE: asyncio.run_in_executorの代わりにasyncio.to_threadが推奨なので変更した。
        return await asyncio.to_thread(self._port_scan, port)

    async def _create_task_with_semaphore(
        self, port: int, semaphore: asyncio.Semaphore
    ) -> dict:
        """_summary_
        _port_scanを非同期処理にするためのラッパー関数
        Args:
            port int: port_number
            semaphore
        Returns:
            dict: {"port": port, "state": state}
        """
        async with semaphore:
            # NOTE: asyncio.run_in_executorの代わりにasyncio.to_threadが推奨なので変更した。
            return await asyncio.to_thread(self._port_scan, port)

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

        if response_packet[TCP].flags == "SA":
            return {"port": port, "state": "open"}
        # RSTパケットが変えてきたときにはclosedとする
        elif response_packet[TCP].flags == "RA":
            return {"port": port, "state": "closed"}
        else:
            return {"port": port, "state": "unknown"}
