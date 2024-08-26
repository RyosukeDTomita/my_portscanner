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
