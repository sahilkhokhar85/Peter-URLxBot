from __future__ import annotations

import time

_STARTED_AT = time.monotonic()


def uptime_seconds() -> int:
    return int(time.monotonic() - _STARTED_AT)


def _unit(value: int, name: str) -> str:
    return f"{value} {name}{'' if value == 1 else 's'}"


def format_uptime(seconds: int) -> str:
    days, rest = divmod(max(0, int(seconds)), 86400)
    hours, rest = divmod(rest, 3600)
    minutes = rest // 60

    parts: list[str] = []
    if days:
        parts.append(_unit(days, "day"))
    if hours:
        parts.append(_unit(hours, "hour"))
    if minutes or not parts:
        parts.append(_unit(minutes, "minute"))
    return ", ".join(parts[:2])
