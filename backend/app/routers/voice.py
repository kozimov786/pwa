from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session

from .. import models
from ..database import get_db
from ..services.voice import parse_voice_command, transcribe_audio

router = APIRouter(prefix="/api/voice", tags=["voice"])


@router.post("/parse")
async def parse_voice(db: Session = Depends(get_db), audio: UploadFile = File(...)):
    audio_bytes = await audio.read()
    text = await transcribe_audio(audio_bytes, audio.filename or "audio.webm")

    products = db.query(models.Product).filter(models.Product.is_active == True).all()  # noqa: E712
    known_names = [p.name for p in products]
    parsed = parse_voice_command(text, known_names)

    product_id = None
    for p in products:
        if p.name == parsed["product_name"]:
            product_id = p.id
            break

    return {**parsed, "product_id": product_id}
