# imports/utils.py
from __future__ import annotations
import re
from datetime import datetime
from django.utils.dateparse import parse_datetime

# 2022-01-01 10:43:32.657 +0300  |  2022-01-01 10:43:32  gibi formatlar için
_TZ_RE = re.compile(
    r"""
    ^\s*
    (?P<date>\d{4}-\d{2}-\d{2})[ T]
    (?P<time>\d{2}:\d{2}:\d{2})       # saniyeye kadar
    (?:\.\d+)?                        # milis/sn varsa yoksay
    (?:\s*[+-]\d{2}:?\d{2})?          # +0300 ya da +03:00 varsa yoksay
    \s*$
    """,
    re.X,
)

def to_seconds_naive(value):
    """
    Gelen değeri 'YYYY-MM-DD HH:MM:SS' formunda, tz'siz (naive) datetime'a çevirir.
    - Milis/sn kırpar
    - +HHMM / +HH:MM tz ekini yoksayar
    - Excel'den gelen datetime objelerinde microsecond ve tz'i temizler
    """
    if value in (None, ""):
        return None

    if isinstance(value, datetime):
        # Excel okuması datetime olarak geldiyse
        return value.replace(microsecond=0, tzinfo=None)

    s = str(value).strip()

    m = _TZ_RE.match(s)
    if m:
        # Tarih-saat kısmını olduğu gibi al (yerel saat olarak yorumluyoruz)
        return datetime.fromisoformat(f"{m['date']} {m['time']}")

    # Fallback: Django parser (ör. 'Z' ya da +03:00 içeren ISO değerler)
    dt = parse_datetime(s)
    if dt is None:
        return None
    return dt.replace(microsecond=0, tzinfo=None)

