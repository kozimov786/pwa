from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/api/expenses", tags=["expenses"])


def _get_or_create_settings(db: Session) -> models.ExpenseSettings:
    settings = db.get(models.ExpenseSettings, 1)
    if not settings:
        settings = models.ExpenseSettings(id=1)
        db.add(settings)
        db.commit()
        db.refresh(settings)
    return settings


@router.get("", response_model=schemas.ExpensesOut)
def get_expenses(db: Session = Depends(get_db)):
    return _get_or_create_settings(db)


@router.put("", response_model=schemas.ExpensesOut)
def update_expenses(payload: schemas.ExpensesUpdate, db: Session = Depends(get_db)):
    settings = _get_or_create_settings(db)
    for field, value in payload.model_dump().items():
        setattr(settings, field, value)
    db.commit()
    db.refresh(settings)
    return settings
