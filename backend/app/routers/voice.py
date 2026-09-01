from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session

from .. import models
from ..database import get_db
from ..services.voice import parse_voice_command, transcribe_audio

router = APIRouter(prefix="/api/voice", tags=["voice"])

NAME_FIELDS = ["name_en", "name_uz", "name_ru", "name_tr", "name_zh"]


@router.post("/parse")
async def parse_voice(db: Session = Depends(get_db), audio: UploadFile = File(...)):
    audio_bytes = await audio.read()
    text = await transcribe_audio(audio_bytes, audio.filename or "audio.webm")

    products = db.query(models.Product).filter(models.Product.is_active == True).all()  # noqa: E712
    # Match against every language's name, since the spoken command could
    # name the product in any of them.
    known_names = [getattr(p, field) for p in products for field in NAME_FIELDS]
    parsed = parse_voice_command(text, known_names)

    product_id = None
    for p in products:
        if parsed["product_name"] in (getattr(p, field) for field in NAME_FIELDS):
            product_id = p.id
            break

    return {**parsed, "product_id": product_id}
