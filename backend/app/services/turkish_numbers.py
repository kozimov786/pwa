"""Turkish integer-to-words with spaces between words, matching how
Turkish banks actually print amounts (e.g. 85000 -> 'seksen beş bin'),
which differs from num2words' concatenated style ('seksenbeşbin').
"""

from __future__ import annotations

ONES = ["", "bir", "iki", "üç", "dört", "beş", "altı", "yedi", "sekiz", "dokuz"]
TENS = ["", "on", "yirmi", "otuz", "kırk", "elli", "altmış", "yetmiş", "seksen", "doksan"]
SCALES = ["", "bin", "milyon", "milyar", "trilyon"]


def _three_digits(n: int) -> list[str]:
    words = []
    hundreds, rest = divmod(n, 100)
    if hundreds:
        if hundreds > 1:
            words.append(ONES[hundreds])
        words.append("yüz")
    tens, ones = divmod(rest, 10)
    if tens:
        words.append(TENS[tens])
    if ones:
        words.append(ONES[ones])
    return words


def number_to_words_tr(n: int) -> str:
    if n == 0:
        return "sıfır"

    groups = []
    temp = n
    while temp > 0:
        groups.append(temp % 1000)
        temp //= 1000

    words: list[str] = []
    for idx in range(len(groups) - 1, -1, -1):
        group = groups[idx]
        if group == 0:
            continue
        group_words = _three_digits(group)
        if idx == 1 and group == 1:
            group_words = []  # "bin", not "bir bin"
        words.extend(group_words)
        if idx > 0:
            words.append(SCALES[idx])
    return " ".join(words)


def turkish_upper(text: str) -> str:
    """str.upper() turns 'i' into dotless 'I', which is wrong in Turkish."""
    return text.replace("i", "İ").replace("ı", "I").upper()
