"""Tiny hand-rolled migrations for the SQLite file — there's no Alembic
here, and Base.metadata.create_all() only creates tables that don't exist
yet, so it silently does nothing when a column is added to a model whose
table already exists on a deployed volume (e.g. Railway). Each function
below is a no-op if the schema is already up to date, so this is safe to
call on every startup."""

from __future__ import annotations

from sqlalchemy import inspect, text
from sqlalchemy.engine import Engine


def _existing_columns(engine: Engine, table: str) -> set[str]:
    inspector = inspect(engine)
    if table not in inspector.get_table_names():
        return set()
    return {c["name"] for c in inspector.get_columns(table)}


def migrate_products_multilang_names(engine: Engine):
    cols = _existing_columns(engine, "products")
    if not cols or "name_en" in cols:
        return  # fresh DB (create_all handles it) or already migrated

    with engine.begin() as conn:
        conn.execute(text("ALTER TABLE products ADD COLUMN name_en VARCHAR"))
        if "name" in cols:
            conn.execute(text("UPDATE products SET name_en = name"))
        for lang_col in ("name_uz", "name_ru", "name_tr", "name_zh"):
            conn.execute(text(f"ALTER TABLE products ADD COLUMN {lang_col} VARCHAR"))
            conn.execute(text(f"UPDATE products SET {lang_col} = name_en"))


def migrate_expense_settings_commission(engine: Engine):
    cols = _existing_columns(engine, "expense_settings")
    if not cols or "commission_cny_per_kg" in cols:
        return
    with engine.begin() as conn:
        conn.execute(text("ALTER TABLE expense_settings ADD COLUMN commission_cny_per_kg FLOAT DEFAULT 0.5"))
        conn.execute(text("UPDATE expense_settings SET commission_cny_per_kg = 0.5 WHERE commission_cny_per_kg IS NULL"))


def run_all(engine: Engine):
    migrate_products_multilang_names(engine)
    migrate_expense_settings_commission(engine)
