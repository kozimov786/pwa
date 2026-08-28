"""Translations for buyer-facing documents (PDF/Excel quotations).
Supported: en, uz, ru, tr, zh. Falls back to English for unknown codes."""

from __future__ import annotations

SUPPORTED_LANGS = ["en", "uz", "ru", "tr", "zh"]

TRANSLATIONS = {
    "en": {
        "product": "Product",
        "weight": "Weight",
        "date": "Date",
        "col_product": "Product",
        "col_destination": "Destination",
        "col_total_kg": "Total kg",
        "col_price_per_kg": "Price/kg (USD)",
        "col_total_cost": "Total cost (USD)",
        "disclaimer": "This quotation is indicative and subject to final contract terms, quality inspection and FX rate at time of payment.",
    },
    "uz": {
        "product": "Mahsulot",
        "weight": "Og'irlik",
        "date": "Sana",
        "col_product": "Mahsulot",
        "col_destination": "Yo'nalish",
        "col_total_kg": "Jami kg",
        "col_price_per_kg": "1 kg narx (USD)",
        "col_total_cost": "Jami maliyet (USD)",
        "disclaimer": "Ushbu taklif indikativ xarakterga ega va yakuniy shartnoma shartlari, sifat tekshiruvi hamda to'lov kunidagi valyuta kursiga bog'liq.",
    },
    "ru": {
        "product": "Товар",
        "weight": "Вес",
        "date": "Дата",
        "col_product": "Товар",
        "col_destination": "Направление",
        "col_total_kg": "Всего кг",
        "col_price_per_kg": "Цена/кг (USD)",
        "col_total_cost": "Общая стоимость (USD)",
        "disclaimer": "Данное предложение носит ориентировочный характер и зависит от условий окончательного контракта, проверки качества и курса валют на дату оплаты.",
    },
    "tr": {
        "product": "Ürün",
        "weight": "Ağırlık",
        "date": "Tarih",
        "col_product": "Ürün",
        "col_destination": "Varış Yeri",
        "col_total_kg": "Toplam kg",
        "col_price_per_kg": "Kg Fiyatı (USD)",
        "col_total_cost": "Toplam Tutar (USD)",
        "disclaimer": "Bu teklif bilgi amaçlıdır; nihai sözleşme şartlarına, kalite kontrolüne ve ödeme günündeki kur oranına tabidir.",
    },
    "zh": {
        "product": "产品",
        "weight": "重量",
        "date": "日期",
        "col_product": "产品",
        "col_destination": "目的地",
        "col_total_kg": "总公斤数",
        "col_price_per_kg": "单价/公斤 (美元)",
        "col_total_cost": "总金额 (美元)",
        "disclaimer": "本报价仅供参考,以最终合同条款、质量检验及付款当日汇率为准。",
    },
}


def t(lang: str, key: str) -> str:
    lang_dict = TRANSLATIONS.get(lang, TRANSLATIONS["en"])
    return lang_dict.get(key, TRANSLATIONS["en"][key])
