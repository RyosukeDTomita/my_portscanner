# cofing:utf-8
import sys
import unittest
from my_portscanner import options


def test_parse_args_default():
    """_summary_
    default option test
    """
    # 必須引数のみ指定
    test_args = [
        "options.py",
        "192.168.1.2",
    ]
    sys.argv = test_args
    args = options.parse_args()
    assert args["target_ip"] == "192.168.1.2"
    assert args["port"] == [22, 80, 443]
    assert args["scan_type"] == "connect"
    assert args["max_rtt_timeout"] == 1000
    assert args["max_parallelism"] is None
    assert args["debug"] is False


def test_parse_args_options():
    """_summary_
    custom option test
    """
    test_args = [
        "options.py",
        "192.168.1.2",
        "-p",
        "80,443",
        "--max-rtt-timeout",
        "1000",
        "-sS",
        "--max-parallelism",
        "32",
        "-d",
    ]
    sys.argv = test_args
    args = options.parse_args()
    assert args["target_ip"] == "192.168.1.2"
    assert args["port"] == [80, 443]
    assert args["scan_type"] == "stealth"
    assert args["max_rtt_timeout"] == 1000
    assert args["max_parallelism"] == 32
    assert args["debug"] is True


def test_parse_args_port_range():
    """
    -p 22-30のようなポートレンジ指定機能のテスト
    """
    test_args = ["options.py", "192.168.1.2", "-sS", "-p", "22-30"]
    sys.argv = test_args
    args = options.parse_args()
    assert args["port"] == [22, 23, 24, 25, 26, 27, 28, 29, 30]


def test_create_port_list_non_digit_list():
    """
    -p hoge,32のようなポートレンジ指定機能のテスト
    """
    port = "hoge,32"
    # ValueErrorが発生することを確認
    try:
        options._create_port_list(port)
    except ValueError as e:
        assert str(e) == "[-p] port list includes non-digit"


def test_create_port_list_non_digit_port_range():
    """
    -p hoge-32のようなポートレンジ指定機能のテスト
    """
    port = "hoge-32"
    # ValueErrorが発生することを確認
    try:
        options._create_port_list(port)
    except ValueError as e:
        assert str(e) == "[-p] port range includes non-digit"


def test_create_port_list_start_larger_than_end():
    """
    -p 32-22のようなポートレンジ指定機能のテスト
    """
    port = "32-22"
    # ValueErrorが発生することを確認
    try:
        options._create_port_list(port)
    except ValueError as e:
        assert str(e) == "[-p] port range start is larger than end"


def test_create_port_list_all_port():
    """
    -p 32-22のようなポートレンジ指定機能のテスト
    """
    port = "-"
    port_list = options._create_port_list(port)
    assert port_list == list(range(0, 65536))


if __name__ == "__main__":
    unittest.main()
