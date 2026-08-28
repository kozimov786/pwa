"""Live USD/CNY exchange rate, refreshed once per calendar day.

'O'sha kungi kurs' — the purchase-price input (CNY) is always converted to
USD using today's rate, fetched from a free public FX API and cached in
memory until the date rolls over. Falls back to a static rate if the
network call fails (e.g. offline dev environment).
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date

import httpx

FX_API_URL = "https://open.er-api.com/v6/latest/USD"

_cache: dict = {"date": None, "rate": None}


@dataclass
class FxRate:
    rate: float
    is_live: bool
    as_of: str


async def get_usd_cny_rate(fallback: float) -> FxRate:
    today = date.today().isoformat()
    if _cache["date"] == today and _cache["rate"]:
        return FxRate(rate=_cache["rate"], is_live=True, as_of=today)

    try:
        async with httpx.AsyncClient(timeout=8) as client:
            resp = await client.get(FX_API_URL)
            resp.raise_for_status()
            rate = float(resp.json()["rates"]["CNY"])
        _cache["date"] = today
        _cache["rate"] = rate
        return FxRate(rate=rate, is_live=True, as_of=today)
    except Exception:
        return FxRate(rate=fallback, is_live=False, as_of=today)
