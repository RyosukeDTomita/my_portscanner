# coding: utf-8
import unittest
from unittest.mock import patch, MagicMock
from scapy.all import IP, TCP
from my_portscanner.scan_tools.SynScan import SynScan


class TestSynScan(unittest.TestCase):
    def setUp(self):
        """
        テスト実行時に毎回実行され，
        socket.socketのmockしたインスタンスを作成する。
        """
        # test data
        self.target_ip = "192.168.150.2"
        self.target_port_list = [22, 80, 443]
        self.expected_open_ports = [22, 443]

        def sr1_side_effect(packet, timeout):
            if packet[TCP].dport in self.expected_open_ports:
                mock_response = MagicMock()
                mock_response.haslayer.return_value = True
                mock_response[TCP].flags = "SA"
                return mock_response
            else:
                mock_response = MagicMock()
                mock_response.haslayer.return_value = False
                return mock_response

        self.sr1_side_effect = (
            sr1_side_effect  # test_runから参照するためにインスタンス変数に格納
        )

    @patch("my_portscanner.scan_tools.SynScan.sr1")
    def test_run(self, mock_sr1):
        scan = SynScan(target_ip=self.target_ip, target_port_list=self.target_port_list)

        mock_sr1.side_effect = self.sr1_side_effect

        open_ports = scan.run()
        print(open_ports)
        self.assertEqual(open_ports, self.expected_open_ports)


if __name__ == "__main__":
    unittest.main()
