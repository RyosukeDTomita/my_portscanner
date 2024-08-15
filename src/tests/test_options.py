# cofing:utf-8
import sys
import pytest
from my_portscanner import options


def test_parse_args():
    test_args = ["options.py", "192.168.1.1", "-oN", "output.txt", "-p", "80,443"]
    sys.argv = test_args
    args = options.parse_args()
    print(args)
    assert args["target_ip"] == "192.168.1.1"
    assert args["file_txt"] == "output.txt"
    assert args["port"] == [80, 443]


if __name__ == "__main__":
    pytest.main()
