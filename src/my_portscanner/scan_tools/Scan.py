# coding: utf-8
from dataclasses import dataclass
import asyncio
from abc import abstractmethod


@dataclass
class Scan:
    target_ip: str
    target_port_list: list[int]
    max_rtt_timeout: int
    max_parallelism: int

    def __init__(self, *args, **kwargs):
        """_summary_

        継承専用のクラスのため，直接インスタンス化できないようにする。
        Raises:
            TypeError: _description_
        """
        if type(self) is Scan:
            raise TypeError(
                "Scan is an abstract class and cannot be instantiated directly"
            )

    def __str__(self) -> str:
        """_summary_
        インスタンスの情報を文字列で返す
        """
        if self.target_port_list == list(range(0, 65536)):
            target_port_list_fmt = "all"
        else:
            target_port_list_fmt = self.target_port_list
        return f"Scan(target_ip={self.target_ip}, target_port_list={target_port_list_fmt}, scan_type={self.__class__.__name__}, max_rtt_timeout={self.max_rtt_timeout}, max_parallelism={self.max_parallelism})"

    @abstractmethod
    def run(self) -> list[dict]:
        pass

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

    @abstractmethod
    def _port_scan(self, port: int) -> dict:
        pass

    def print_result(self) -> None:
        """
        port scanの結果を表示する
        """
        # 出力が100行を超えそうなときは，closed portsを非表示にする。
        if len(self.scan_result) > 100:
            self.scan_result = [
                port_info for port_info in self.scan_result if port_info["state"] != "closed"
            ]
        # port6桁+/tcpで10桁
        print(f"{"PORT":<10} {"STATE":<8} SERVICE")
        for port_info in self.scan_result:
            print(
                f"{port_info["port"]}/tcp".ljust(10)
                + " "
                + f"{port_info["state"]:<8} unknown"
            )
