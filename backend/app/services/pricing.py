"""Landed-price cascade engine.

Route modeled:
  China (ex-works, CNY) -> Osh, Kyrgyzstan (CPT/DAP)
                         -> Tashkent, Uzbekistan (DAP)
                            -> Gaziantep / Mersin, Turkey (DAP)
                            -> Baku, Azerbaijan (DAP)
                            -> Romania (DAP, quoted in USD & EUR)

All transit-leg costs are USD/ton. The product's base price is stored in
CNY/ton and converted using the live/settings FX rate.
"""

from __future__ import annotations

from dataclasses import dataclass

from ..models import ExpenseSettings, Product


@dataclass
class Leg:
    destination: str
    incoterm: str
    price_per_ton_usd: float
    price_per_ton_eur: float | None = None


def calculate_landed_prices(
    product: Product,
    expenses: ExpenseSettings,
    tonnage: float,
    margin_usd_per_ton: float = 0.0,
) -> tuple[float, list[Leg]]:
    base_usd_per_ton = (product.price_cny_per_ton / expenses.usd_cny_rate) + margin_usd_per_ton

    osh_price = base_usd_per_ton + expenses.cn_docs + expenses.cn_osh_freight + expenses.kg_transit
    tashkent_price = osh_price + expenses.osh_tashkent_freight + expenses.uzb_transit
    antep_price = tashkent_price + expenses.tashkent_antep_freight
    baku_price = tashkent_price + expenses.tashkent_baku_freight
    romania_price_usd = tashkent_price + expenses.tashkent_romania_freight
    romania_price_eur = romania_price_usd * expenses.usd_eur_rate

    legs = [
        Leg("Osh", "CPT/DAP", round(osh_price, 2)),
        Leg("Tashkent", "DAP", round(tashkent_price, 2)),
        Leg("Gaziantep / Mersin", "DAP", round(antep_price, 2)),
        Leg("Baku", "DAP", round(baku_price, 2)),
        Leg("Romania", "DAP", round(romania_price_usd, 2), round(romania_price_eur, 2)),
    ]
    return round(base_usd_per_ton, 2), legs


def legs_to_response(legs: list[Leg], tonnage: float) -> list[dict]:
    out = []
    for leg in legs:
        out.append(
            {
                "destination": leg.destination,
                "incoterm": leg.incoterm,
                "price_per_ton_usd": leg.price_per_ton_usd,
                "price_per_ton_eur": leg.price_per_ton_eur,
                "total_usd": round(leg.price_per_ton_usd * tonnage, 2),
                "total_eur": round(leg.price_per_ton_eur * tonnage, 2) if leg.price_per_ton_eur else None,
            }
        )
    return out
