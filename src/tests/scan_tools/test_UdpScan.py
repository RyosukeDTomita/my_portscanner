from io import StringIO
import sys
import unittest
from unittest.mock import patch, MagicMock
from scapy.all import UDP, ICMP
from my_portscanner.scan_tools.UdpScan import UdpScan


class TestUdpScan(unittest.TestCase):
    """
    NOTE: print_result()の一部テストはtest_ConnectScan.pyと共通なので省略
    """

    def setUp(self):
        """
        テスト実行時に毎回実行され，
        socket.socketのmockしたインスタンスを作成する。
        """
        # 共通のテストデータ
        self.target_ip = "192.168.150.2"
        self.target_port_list = [68, 123, 135]
        self.expected_open_filterd_ports = [68, 123]  # dhcp, ntp
        self.expected_closed_ports = [135]  # msrpc
        self.max_rtt_timeout = 100
        self.max_parallelism = 16

        def sr1_side_effect(packet, timeout):
            if packet[UDP].dport in self.expected_open_filterd_ports:
                return None
            elif packet[UDP].dport in self.expected_closed_ports:
                mock_response = MagicMock()
                # ICMP layerがあるかどうか
                mock_response.haslayer.side_effect = lambda x: x == ICMP
                # mock_response[ICMP].type = 3
                # mock_response[ICMP].code = 3
                mock_icmp = MagicMock()
                mock_icmp.type = 3
                mock_icmp.code = 3
                mock_response.getlayer.return_value = mock_icmp
                return mock_response

        self.sr1_side_effect = sr1_side_effect

    @patch("my_portscanner.scan_tools.UdpScan.sr1")
    def test_port_scan(self, mock_sr1):
        mock_sr1.side_effect = self.sr1_side_effect

        scan = UdpScan(
            target_ip=self.target_ip,
            target_port_list=self.target_port_list,
            max_rtt_timeout=self.max_rtt_timeout,
            max_parallelism=self.max_parallelism,
            no_ping=False,
        )
        scan_result = []
        for port in self.target_port_list:
            scan_result.append(scan._port_scan(port))
        self.assertEqual(
            scan_result,
            [
                {"port": 68, "state": "open|filtered"},
                {"port": 123, "state": "open|filtered"},
                {"port": 135, "state": "closed"},
            ],
        )

    def test_print_result(self):
        """_summary_
        print_resultで想定通りの出力がでるか確認するテスト
        """
        scan = UdpScan(
            target_ip=self.target_ip,
            target_port_list=self.target_port_list,
            max_rtt_timeout=self.max_rtt_timeout,
            max_parallelism=self.max_parallelism,
            no_ping=True,
        )
        scan.scan_result = [
            {"port": 68, "state": "open|filtered"},
            {"port": 123, "state": "open|filtered"},
            {"port": 135, "state": "closed"},
        ]

        # 標準出力をキャプチャ
        captured_output = StringIO()
        sys.stdout = captured_output

        scan.print_result()

        # 標準出力の内容を取得
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue().strip()

        expected_output = (
            f"{'PORT':<10} {'STATE':<13} SERVICE\n"
            f"{'68/udp':<10}" + " " + f"{'open|filtered':<13} unknown\n"
            f"{'123/udp':<10}" + " " + f"{'open|filtered':<13} unknown\n"
            f"{'135/udp':<10}" + " " + f"{'closed':<13} unknown"
        )

        self.assertEqual(output, expected_output)


if __name__ == "__main__":
    unittest.main()
