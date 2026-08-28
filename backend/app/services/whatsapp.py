from __future__ import annotations

import os

import httpx

GREEN_API_ID = os.getenv("GREEN_API_ID_INSTANCE", "")
GREEN_API_TOKEN = os.getenv("GREEN_API_TOKEN", "")
GREEN_API_GROUP_ID = os.getenv("GREEN_API_GROUP_ID", "")
GREEN_API_BASE = f"https://api.green-api.com/waInstance{GREEN_API_ID}"


async def send_text_message(message: str) -> dict:
    url = f"{GREEN_API_BASE}/sendMessage/{GREEN_API_TOKEN}"
    payload = {"chatId": GREEN_API_GROUP_ID, "message": message}
    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.post(url, json=payload)
        resp.raise_for_status()
        return resp.json()


async def send_file_bytes(file_bytes: bytes, filename: str, caption: str = "") -> dict:
    url = f"{GREEN_API_BASE}/sendFileByUpload/{GREEN_API_TOKEN}"
    files = {"file": (filename, file_bytes)}
    data = {"chatId": GREEN_API_GROUP_ID, "caption": caption}
    async with httpx.AsyncClient(timeout=60) as client:
        resp = await client.post(url, data=data, files=files)
        resp.raise_for_status()
        return resp.json()


async def dispatch_to_group(message: str, attachments: list[tuple[bytes, str]] | None = None) -> dict:
    """Send a text message and optional list of (bytes, filename) attachments
    to the configured WhatsApp group via Green-API."""
    results = {"message": await send_text_message(message), "files": []}
    for file_bytes, filename in attachments or []:
        results["files"].append(await send_file_bytes(file_bytes, filename))
    return results
