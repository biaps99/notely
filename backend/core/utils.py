from datetime import datetime, timezone


def get_now_utc() -> "datetime":
    return datetime.now(timezone.utc)
