"""Landed-price cascade engine — all figures in USD per kg.

Route modeled:
  China (purchase price, CNY/kg) -> Osh, Kyrgyzstan (CPT/DAP)
                                  -> Tashkent, Uzbekistan (DAP)
                                     -> any number of final destinations,
                                        each user-managed in Settings
                                        (Gaziantep/Mersin, Azerbaijan-Baku,
                                        Romania, Syria, ...)

Every leg is a FIXED total cost per shipment (e.g. one truck load), not a
per-ton rate — that's how freight is actually quoted for this route. So
every leg cost is divided by the shipment's real weight_kg here, which
correctly makes heavier shipments cheaper per kg on fixed freight legs.
"""

from __future__ import annotations

from dataclasses import dataclass

from ..models import Destination, ExpenseSettings


@dataclass
class Leg:
    destination: str
    price_per_kg_usd: float


def calculate_landed_prices(
    expenses: ExpenseSettings,
    destinations: list[Destination],
    price_cny_per_kg: float,
    usd_cny_rate: float,
    weight_kg: float,
    margin_usd_per_kg: float = 0.0,
) -> tuple[float, list[Leg]]:
    base_usd_per_kg = (price_cny_per_kg / usd_cny_rate) + margin_usd_per_kg

    def per_kg(total_usd: float) -> float:
        return total_usd / weight_kg

    cn_docs = per_kg(expenses.cn_docs_cny / usd_cny_rate)
    cn_osh_freight = per_kg(expenses.cn_osh_freight_usd)
    kg_transit = per_kg(expenses.kg_transit_usd)
    osh_tashkent_freight = per_kg(expenses.osh_tashkent_freight_usd)
    uzb_transit = per_kg(expenses.uzb_transit_usd)

    osh_price = base_usd_per_kg + cn_docs + cn_osh_freight + kg_transit
    tashkent_price = osh_price + osh_tashkent_freight + uzb_transit

    legs = [
        Leg("Osh (CPT/DAP)", round(osh_price, 4)),
        Leg("Tashkent (DAP)", round(tashkent_price, 4)),
    ]
    for dest in destinations:
        if not dest.is_active:
            continue
        price = tashkent_price + per_kg(dest.freight_usd_total)
        legs.append(Leg(f"{dest.name} ({dest.incoterm})", round(price, 4)))

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
