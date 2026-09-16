"""
Lightweight Gregorian <-> Hijri (tabular Islamic calendar) conversion.
Pure Python, no external dependency required — keeps deployment simple
and avoids relying on a third-party package that might not build on
every host.

Note: this is the standard *tabular* Islamic calendar (arithmetic,
30-year cycle). It can be off by a day from local moonsighting-based
dates in some regions/months. An "adjustment" of -1/0/+1 day is
exposed in the app so a center can tune it to match local moonsighting
announcements.
"""

from datetime import date, timedelta

HIJRI_MONTH_NAMES = [
    "Muharram", "Safar", "Rabi' al-Awwal", "Rabi' al-Thani",
    "Jumada al-Awwal", "Jumada al-Thani", "Rajab", "Sha'ban",
    "Ramadan", "Shawwal", "Dhu al-Qi'dah", "Dhu al-Hijjah",
]

_ISLAMIC_EPOCH = 1948439.5  # Julian day of 1 Muharram, 1 AH (civil/tabular)


def _is_hijri_leap(year: int) -> bool:
    return (11 * year + 14) % 30 < 11


def _hijri_to_jd(year: int, month: int, day: int) -> float:
    return (
        day
        + 29.5 * (month - 1)
        + (month // 2) * 0.5
        + (year - 1) * 354.367
        + _ISLAMIC_EPOCH
        - 1
        + ((3 + 11 * year) % 30) * 0  # keep formula stable; refined below
    )


def _gregorian_to_jd(y: int, m: int, d: int) -> int:
    a = (14 - m) // 12
    y2 = y + 4800 - a
    m2 = m + 12 * a - 3
    return d + (153 * m2 + 2) // 5 + 365 * y2 + y2 // 4 - y2 // 100 + y2 // 400 - 32045


def _jd_to_gregorian(jd: int):
    a = jd + 32044
    b = (4 * a + 3) // 146097
    c = a - (146097 * b) // 4
    d_ = (4 * c + 3) // 1461
    e = c - (1461 * d_) // 4
    m_ = (5 * e + 2) // 153
    day = e - (153 * m_ + 2) // 5 + 1
    month = m_ + 3 - 12 * (m_ // 10)
    year = 100 * b + d_ - 4800 + m_ // 10
    return year, month, day


def gregorian_to_hijri(g: date, adjustment: int = 0):
    """Return (hijri_year, hijri_month, hijri_day) for a Gregorian date."""
    jd = _gregorian_to_jd(g.year, g.month, g.day) + adjustment
    jd = jd - _ISLAMIC_EPOCH
    year = int((30 * jd + 10646) // 10631)
    month_start_jd = _ISLAMIC_EPOCH + _year_start_offset(year)
    # Iterate months within the year to find the correct month/day
    remaining = jd - _year_start_offset(year)
    month = 1
    while month <= 12:
        length = 30 if month % 2 == 1 else 29
        if month == 12 and _is_hijri_leap(year):
            length = 30
        if remaining < length:
            break
        remaining -= length
        month += 1
    day = int(remaining) + 1
    return year, month, day


def _year_start_offset(year: int) -> float:
    # Days elapsed from epoch to the start of the given Hijri year
    return 354 * (year - 1) + (3 + 11 * (year - 1)) // 30


def hijri_to_gregorian(year: int, month: int, day: int, adjustment: int = 0) -> date:
    days = _year_start_offset(year)
    for m in range(1, month):
        length = 30 if m % 2 == 1 else 29
        if m == 12 and _is_hijri_leap(year):
            length = 30
        days += length
    days += day - 1
    jd = int(_ISLAMIC_EPOCH + days) - adjustment
    y, m_, d_ = _jd_to_gregorian(jd)
    return date(y, m_, d_)


def month_length(year: int, month: int) -> int:
    if month == 12 and _is_hijri_leap(year):
        return 30
    return 30 if month % 2 == 1 else 29
