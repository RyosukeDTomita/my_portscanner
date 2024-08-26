from io import StringIO
import sys
import unittest
from unittest.mock import patch
from my_portscanner.scan_tools.ConnectScan import ConnectScan


class TestConnectScan(unittest.TestCase):
    def setUp(self):
        """
        テスト実行時に毎回実行され，
        socket.socketのmockしたインスタンスを作成する。
        """
        # 共通のテストデータ
        self.target_ip = "192.168.150.2"
        self.target_port_list = [22, 80, 443, 8080]
        self.expected_open_ports = [80, 443]
        self.expected_closed_ports = [8080]
        self.expected_filterd_ports = [22]
        self.max_rtt_timeout = 100
        self.max_parallelism = 16

    @patch("my_portscanner.scan_tools.ConnectScan.socket.socket")
    def test_port_scan(self, mock_socket):
        def connext_ex_side_effect(target_tuple):
            _, port = target_tuple[0], target_tuple[1]
            if port in self.expected_open_ports:
                return 0
            elif port in self.expected_closed_ports:
                return 111
            else:
                return 11

        mock_socket_instance = mock_socket.return_value
        mock_socket_instance.connect_ex.side_effect = connext_ex_side_effect

        scan = ConnectScan(
            target_ip=self.target_ip,
            target_port_list=self.target_port_list,
            max_rtt_timeout=self.max_rtt_timeout,
            max_parallelism=self.max_parallelism,
        )
        scan_result = []
        for port in self.target_port_list:
            scan_result.append(scan._port_scan(port))
        self.assertEqual(
            scan_result,
            [
                {"port": 22, "state": "filtered"},
                {"port": 80, "state": "open"},
                {"port": 443, "state": "open"},
                {"port": 8080, "state": "closed"},
            ],
        )

    def test_print_result(self):
        """_summary_
        print_resultで想定通りの出力がでるか確認するテスト
        """
        scan = ConnectScan(
            target_ip=self.target_ip,
            target_port_list=self.target_port_list,
            max_rtt_timeout=self.max_rtt_timeout,
            max_parallelism=self.max_parallelism,
        )
        scan.scan_result = [
            {"port": 22, "state": "filtered"},
            {"port": 80, "state": "open"},
            {"port": 443, "state": "open"},
            {"port": 8080, "state": "closed"},
        ]

        # 標準出力をキャプチャ
        captured_output = StringIO()
        sys.stdout = captured_output

        scan.print_result()

        # 標準出力の内容を取得
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue().strip()

        expected_output = (
            f"{'PORT':<10} {'STATE':<8} SERVICE\n"
            f"{'22/tcp':<10}" + " " + f"{'filtered':<8} unknown\n"
            f"{'80/tcp':<10}" + " " + f"{'open':<8} unknown\n"
            f"{'443/tcp':<10}" + " " + f"{'open':<8} unknown\n"
            f"{'8080/tcp':<10}" + " " + f"{'closed':<8} unknown"
        )

        self.assertEqual(output, expected_output)

    def test_print_result_remove_closed_ports_when_scan_result_is_long(self):
        """_summary_
        出力が100行を超える時はclosed portsを非表示になることを確認するテスト
        """
        scan = ConnectScan(
            target_ip=self.target_ip,
            target_port_list=self.target_port_list,
            max_rtt_timeout=self.max_rtt_timeout,
            max_parallelism=self.max_parallelism,
        )

        # 100行以上のテストデータを作成
        scan.scan_result = [{"port": i, "state": "closed"} for i in range(101)]

        # 標準出力をキャプチャ
        captured_output = StringIO()
        sys.stdout = captured_output

        scan.print_result()

        # 標準出力の内容を取得
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue().strip()

        # 何も表示されないことを確認
        expected_output = f"{'PORT':<10} {'STATE':<8} SERVICE"
        self.assertEqual(output, expected_output)


if __name__ == "__main__":
    unittest.main()
