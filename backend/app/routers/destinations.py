from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/api/destinations", tags=["destinations"])


@router.get("", response_model=list[schemas.DestinationOut])
def list_destinations(db: Session = Depends(get_db)):
    return (
        db.query(models.Destination)
        .order_by(models.Destination.sort_order, models.Destination.id)
        .all()
    )


@router.post("", response_model=schemas.DestinationOut, status_code=201)
def create_destination(payload: schemas.DestinationCreate, db: Session = Depends(get_db)):
    existing = db.query(models.Destination).filter(models.Destination.name == payload.name).first()
    if existing:
        raise HTTPException(status_code=409, detail="Destination with this name already exists")
    destination = models.Destination(**payload.model_dump())
    db.add(destination)
    db.commit()
    db.refresh(destination)
    return destination


@router.put("/{destination_id}", response_model=schemas.DestinationOut)
def update_destination(destination_id: int, payload: schemas.DestinationUpdate, db: Session = Depends(get_db)):
    destination = db.get(models.Destination, destination_id)
    if not destination:
        raise HTTPException(status_code=404, detail="Destination not found")
    for field, value in payload.model_dump().items():
        setattr(destination, field, value)
    db.commit()
    db.refresh(destination)
    return destination


@router.delete("/{destination_id}", status_code=204)
def delete_destination(destination_id: int, db: Session = Depends(get_db)):
    destination = db.get(models.Destination, destination_id)
    if not destination:
        raise HTTPException(status_code=404, detail="Destination not found")
    db.delete(destination)
    db.commit()
