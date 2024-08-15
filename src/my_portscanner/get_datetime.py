# coding: utf-8
from datetime import datetime
import pytz


def get_datetime():
    japan_tz = pytz.timezone("Asia/Tokyo")
    dt = datetime(2024, 8, 15, 10, 5, tzinfo=japan_tz)
    print(dt.strftime("%Y-%m-%d %H:%M %Z"))


if __name__ == "__main__":
    get_datetime()
