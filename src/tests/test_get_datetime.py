# coding: utf-8
from freezegun import freeze_time
from my_portscanner import get_datetime


def test_get_datetime():
    """
    現在の日時を取得するテスト
    """
    # NOTE: datetime.datetimeがimmutable型なので，インスタンス作成後にその状態を変更できない。そのためfreeze_timeを使ってmockする
    with freeze_time("2038-01-19 03:14:07"):
        datetime = get_datetime.get_datetime_now()
        assert datetime == "2038-01-19 12:14 JST"


if __name__ == "__main__":
    test_get_datetime()
