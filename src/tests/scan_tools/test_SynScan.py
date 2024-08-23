# coding: utf-8
from io import StringIO
import sys
import unittest
from unittest.mock import patch, MagicMock
from scapy.all import TCP
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
        self.max_rtt_timeout = 100

        def sr1_side_effect(packet, timeout):
            # 管理者権限がない場合PermissionErrorを発生させる
            # NOTE: UID=0の時rootまたはsudo
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
        scan = SynScan(
            target_ip=self.target_ip,
            target_port_list=self.target_port_list,
            max_rtt_timeout=self.max_rtt_timeout,
        )

        mock_sr1.side_effect = self.sr1_side_effect

        open_ports = scan.run()
        print(open_ports)
        self.assertEqual(open_ports, self.expected_open_ports)

    @patch("my_portscanner.scan_tools.SynScan.sr1")
    def test_run_raise_permission_error(self, mock_sr1):
        """_summary_
        SynScan.run()実行時にSYNパケットを作るのにroot権限が必要なため，PermissionErrorが発生時の出力をチェックする。

        Args:
            mock_sr1
        """
        expected_output = (
            "You requested a scan type which requires root privileges.\nQUITTING!"
        )

        scan = SynScan(
            target_ip=self.target_ip,
            target_port_list=self.target_port_list,
            max_rtt_timeout=self.max_rtt_timeout,
        )

        # NOTE: mock_getuid.return_valueによってuid=0以外にmockしてもうまくPermissionErrorを発生させることができなかったので直接PermissionErrorを発生させる
        mock_sr1.side_effect = PermissionError

        # 標準出力をキャプチャ
        captured_output = StringIO()
        sys.stdout = captured_output

        # PermissionErrorが発生するため，sys.exit(1)が呼ばれる
        try:
            with self.assertRaises(SystemExit) as e:
                scan.run()
            self.assertEqual(e.exception.code, 1)

        # 他のtestに影響を与えないように標準出力を元に戻す
        finally:
            sys.stdout = sys.__stdout__

        output = captured_output.getvalue().strip()
        assert output == expected_output


if __name__ == "__main__":
    unittest.main()
