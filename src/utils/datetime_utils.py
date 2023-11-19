# Created by https://t.me/vlasovdev datetime_utils file | Создано https://t.me/vlasovdev datetime_utils file


from datetime import datetime
from typing import Tuple

import pytz


def current_datetime_with_tz() -> datetime:
    return datetime.now(pytz.timezone("Europe/Moscow"))


def current_date_with_tz() -> datetime:
    return datetime.today().date()


def format_datetime(datetime_to_format: datetime | None = None) -> datetime:
    if not datetime_to_format:
        datetime_to_format = current_datetime_with_tz()
    return datetime_to_format.strftime("%Y-%m-%d %H:%M:%S")
