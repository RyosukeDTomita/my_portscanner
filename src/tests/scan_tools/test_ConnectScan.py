from io import StringIO
import sys
import unittest
from unittest.mock import patch, MagicMock
from my_portscanner.scan_tools.ConnectScan import ConnectScan


class TestConnectScan(unittest.TestCase):
    def setUp(self):
        """
        テスト実行時に毎回実行され，
        socket.socketのmockしたインスタンスを作成する。
        """
        # 共通のテストデータ
        self.target_ip = "192.168.150.2"
        self.target_port_list = [22, 80, 443]
        self.expected_open_ports = [22, 443]

        # mock_socket_instanceの作成
        self.mock_socket_instance = MagicMock()

        # connect_exの戻り値を設定
        def connect_ex_side_effect(address):
            ip, port = address
            if port in self.expected_open_ports:
                return 0  # open
            else:
                return 1  # close

        self.mock_socket_instance.connect_ex.side_effect = connect_ex_side_effect
        return

    @patch("my_portscanner.scan_tools.ConnectScan.socket.socket")
    def test_run(self, mock_socket):
        mock_socket.return_value = self.mock_socket_instance

        scan = ConnectScan(
            target_ip=self.target_ip, target_port_list=self.target_port_list
        )
        open_ports = scan.run()

        self.assertEqual(open_ports, self.expected_open_ports)

    @patch("my_portscanner.scan_tools.ConnectScan.socket.socket")
    def test_print_result(self, mock_socket):
        mock_socket.return_value = self.mock_socket_instance

        scan = ConnectScan(
            target_ip=self.target_ip, target_port_list=self.target_port_list
        )
        scan.run()

        # 標準出力をキャプチャ
        captured_output = StringIO()
        sys.stdout = captured_output

        # print_resultメソッドの実行
        scan.print_result()

        # 標準出力の内容を取得
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue().strip()

        # 期待される出力
        expected_output = "PORT       STATE SERVICE\n22/tcp     open  unknown\n443/tcp    open  unknown"

        self.assertEqual(output, expected_output)


if __name__ == "__main__":
    unittest.main()
