from __future__ import annotations

import os
import re

from openai import AsyncOpenAI

_client: AsyncOpenAI | None = None


def get_client() -> AsyncOpenAI:
    global _client
    if _client is None:
        _client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    return _client


async def transcribe_audio(file_bytes: bytes, filename: str) -> str:
    client = get_client()
    # openai SDK expects a file-like object with a .name attribute for format detection
    buf = _NamedBytesIO(file_bytes, filename)
    transcript = await client.audio.transcriptions.create(
        model="whisper-1",
        file=buf,
    )
    return transcript.text


class _NamedBytesIO:
    """Minimal binary-file wrapper carrying a filename, as required by the
    OpenAI SDK to infer the audio container format."""

    def __init__(self, data: bytes, name: str):
        import io

        self._buf = io.BytesIO(data)
        self.name = name

    def read(self, *a, **kw):
        return self._buf.read(*a, **kw)

    def seek(self, *a, **kw):
        return self._buf.seek(*a, **kw)


TONNAGE_RE = re.compile(r"(\d+(?:[.,]\d+)?)\s*(?:tonna|tonnes?|tons?|t\b)", re.IGNORECASE)
CURRENCY_RE = re.compile(r"\b(usd|dollar|dollar|cny|yuan|euro|eur|so'?m)\b", re.IGNORECASE)


def parse_voice_command(text: str, known_products: list[str]) -> dict:
    """Best-effort extraction of product name / tonnage / currency from a
    free-form transcribed voice command, e.g.
    'Kabuklu 33 uchun 21 tonna narxni hisobla dollarda'."""
    result: dict = {"raw_text": text, "product_name": None, "tonnage": None, "currency": None}

    lowered = text.lower()
    for name in known_products:
        if name.lower() in lowered:
            result["product_name"] = name
            break

    tonnage_match = TONNAGE_RE.search(text)
    if tonnage_match:
        result["tonnage"] = float(tonnage_match.group(1).replace(",", "."))

    currency_match = CURRENCY_RE.search(text)
    if currency_match:
        token = currency_match.group(1).lower()
        if token in ("usd", "dollar"):
            result["currency"] = "USD"
        elif token in ("cny", "yuan"):
            result["currency"] = "CNY"
        elif token in ("euro", "eur"):
            result["currency"] = "EUR"
        elif "so" in token:
            result["currency"] = "UZS"

    return result
