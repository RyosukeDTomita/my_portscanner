# cofing:utf-8
import sys
from my_portscanner import options


def test_parse_args():
    test_args = ["options.py", "192.168.1.2", "-p", "80,443"]
    sys.argv = test_args
    args = options.parse_args()
    assert args["target_ip"] == "192.168.1.2"
    assert args["port"] == [80, 443]


def test_parse_args_port_range():
    """
    -p 22-30のようなポートレンジ指定機能のテスト
    """
    test_args = ["options.py", "192.168.1.2", "-sS", "-p", "22-30"]
    sys.argv = test_args
    args = options.parse_args()
    assert args["port"] == [22, 23, 24, 25, 26, 27, 28, 29, 30]


if __name__ == "__main__":
    test_parse_args()
    test_parse_args_port_range()
