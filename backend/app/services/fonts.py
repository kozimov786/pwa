"""Unicode font setup for reportlab PDFs.

The base-14 PDF fonts (Helvetica etc.) only cover Latin-1/WinAnsi, which is
fine for English and Uzbek but breaks Turkish (ğ, ş, ı) and Russian
(Cyrillic). Chinese needs a CJK font entirely. This module registers:
  - "NotoSans" / "NotoSans-Bold": a bundled TTF covering Latin Extended +
    Cyrillic, used for tr/ru (and reused for en/uz for visual consistency).
  - "STSong-Light": reportlab's built-in CJK CID font (no file needed),
    used for zh.
"""

from __future__ import annotations

import os

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.pdfbase.ttfonts import TTFont

_FONTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "fonts")
_NOTOSANS_PATH = os.path.join(_FONTS_DIR, "NotoSans.ttf")

_registered = False


def _ensure_registered():
    global _registered
    if _registered:
        return
    if os.path.exists(_NOTOSANS_PATH):
        pdfmetrics.registerFont(TTFont("NotoSans", _NOTOSANS_PATH))
        pdfmetrics.registerFontFamily("NotoSans", normal="NotoSans", bold="NotoSans")
    pdfmetrics.registerFont(UnicodeCIDFont("STSong-Light"))
    _registered = True


def font_for_lang(lang: str) -> str:
    """Returns the registered font name that can render the given language."""
    _ensure_registered()
    if lang == "zh":
        return "STSong-Light"
    if lang in ("ru", "tr") and os.path.exists(_NOTOSANS_PATH):
        return "NotoSans"
    return "Helvetica"
