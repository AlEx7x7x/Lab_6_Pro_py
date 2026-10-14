"""Конфігурація: мінімальний stock та режим оплати."""

import os
from pathlib import Path

import yaml

DEFAULT_MIN_STOCK = 5


def get_payment_mode() -> str:
    return os.getenv("PAYMENT_MODE", "sandbox")


def get_min_stock() -> int:
    raw = os.getenv("MIN_STOCK")
    if raw is None:
        return DEFAULT_MIN_STOCK
    try:
        value = int(raw)
    except ValueError as error:
        raise ValueError("MIN_STOCK must be an integer") from error
    if value < 0:
        raise ValueError("MIN_STOCK cannot be negative")
    return value


def load_config(path: Path) -> dict:
    if not path.exists():
        raise FileNotFoundError(f"Config not found: {path}")
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    
    min_stock = data.get("min_stock")
    currency = data.get("currency")
    categories = data.get("categories")
    
    return {
        "min_stock": int(min_stock) if min_stock is not None else DEFAULT_MIN_STOCK,
        "currency": str(currency) if currency is not None else "UAH",
        "categories": list(categories) if categories is not None else [],
    }
