from datetime import datetime

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
DATETIME_URL_FORMAT = "%Y%m%d%H%M%S"


def datetime_to_string(dt: datetime) -> str:
    return dt.strftime(DATETIME_FORMAT)


def parse_datetime_string(dt_string: str) -> datetime:
    return datetime.strptime(dt_string, DATETIME_FORMAT)


def datetime_to_url(dt: datetime) -> str:
    return dt.strftime(DATETIME_URL_FORMAT)


def parse_datetime_url(dt_url: str) -> datetime | None:
    try:
        return datetime.strptime(dt_url, DATETIME_URL_FORMAT)
    except Exception:
        return None
