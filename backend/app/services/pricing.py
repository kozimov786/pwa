"""Landed-price cascade engine — all figures in USD per kg.

Route modeled:
  China (purchase price, CNY/kg) -> Osh, Kyrgyzstan (CPT/DAP)
                                  -> Tashkent, Uzbekistan (DAP)
                                     -> Gaziantep / Mersin, Turkey (DAP)
                                     -> Baku, Azerbaijan (DAP)
                                     -> Romania (DAP)

Transit-leg costs are configured in USD/ton (the trade-standard unit) and
converted to USD/kg internally so the whole cascade — and the UI — works
in a single unit: kilograms.
"""

from __future__ import annotations

from dataclasses import dataclass

from ..models import ExpenseSettings

KG_PER_TON = 1000.0


@dataclass
class Leg:
    destination: str
    price_per_kg_usd: float


def calculate_landed_prices(
    expenses: ExpenseSettings,
    price_cny_per_kg: float,
    usd_cny_rate: float,
    margin_usd_per_kg: float = 0.0,
) -> tuple[float, list[Leg]]:
    base_usd_per_kg = (price_cny_per_kg / usd_cny_rate) + margin_usd_per_kg

    cn_docs = expenses.cn_docs / KG_PER_TON
    cn_osh_freight = expenses.cn_osh_freight / KG_PER_TON
    kg_transit = expenses.kg_transit / KG_PER_TON
    osh_tashkent_freight = expenses.osh_tashkent_freight / KG_PER_TON
    uzb_transit = expenses.uzb_transit / KG_PER_TON
    tashkent_antep_freight = expenses.tashkent_antep_freight / KG_PER_TON
    tashkent_romania_freight = expenses.tashkent_romania_freight / KG_PER_TON
    tashkent_baku_freight = expenses.tashkent_baku_freight / KG_PER_TON

    osh_price = base_usd_per_kg + cn_docs + cn_osh_freight + kg_transit
    tashkent_price = osh_price + osh_tashkent_freight + uzb_transit
    antep_price = tashkent_price + tashkent_antep_freight
    baku_price = tashkent_price + tashkent_baku_freight
    romania_price = tashkent_price + tashkent_romania_freight

    legs = [
        Leg("Osh (CPT/DAP)", round(osh_price, 4)),
        Leg("Tashkent (DAP)", round(tashkent_price, 4)),
        Leg("Gaziantep / Mersin (DAP)", round(antep_price, 4)),
        Leg("Baku (DAP)", round(baku_price, 4)),
        Leg("Romania (DAP)", round(romania_price, 4)),
    ]
    return round(base_usd_per_kg, 4), legs


def legs_to_response(legs: list[Leg], weight_kg: float) -> list[dict]:
    return [
        {
            "destination": leg.destination,
            "price_per_kg_usd": leg.price_per_kg_usd,
            "total_usd": round(leg.price_per_kg_usd * weight_kg, 2),
        }
        for leg in legs
    ]
