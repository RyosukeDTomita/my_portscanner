# coding: utf-8
import pytest
from unittest.mock import patch, mock_open
from my_portscanner import toml_parser


def test_get_project_version():
    """
    pyproject.tomlのproject.versionを取得するテスト
    """

    # pyproject.tomlをmock
    # NOTE: モックをバイナリとして読み込む必要があるため，bをつける
    mock_toml_content = b"""
    [project]
    version = "1.0.0"
    """
    # toml_parser.get_project_version()の一部の関数をmock
    with patch("builtins.open", mock_open(read_data=mock_toml_content)):
        with patch("os.path.abspath", return_value="/fake/path/toml_parser.py"):
            with patch("os.path.dirname", return_value="/fake/path"):
                version = toml_parser.get_project_version()
                assert version == "1.0.0"


def test_get_project_version_no_version():
    mock_toml_content = b"""
    [project]
    """

    with patch("builtins.open", mock_open(read_data=mock_toml_content)):
        with patch("os.path.abspath", return_value="/fake/path/toml_parser.py"):
            with patch("os.path.dirname", return_value="/fake/path"):
                version = toml_parser.get_project_version()
                assert version == "No version found"


if __name__ == "__main__":
    pytest.main()
