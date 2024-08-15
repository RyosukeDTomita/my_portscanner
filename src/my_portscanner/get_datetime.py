# coding: utf-8
from datetime import datetime
import pytz


def get_datetime_now() -> str:
    """_summary_

    Returns:
        str: "YYYY-MM-DD HH:MM JST"
    """
    japan_tz = pytz.timezone("Asia/Tokyo")
    dt = datetime.now(japan_tz)
    return dt.strftime("%Y-%m-%d %H:%M %Z")


if __name__ == "__main__":
    now = get_datetime_now()
    print(f"Current datetime: {now}")
