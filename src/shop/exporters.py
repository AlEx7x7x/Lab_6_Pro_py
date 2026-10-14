import json
import os
from pathlib import Path

from shop.models import Product


def export_order(order: dict, path: Path) -> None:
    path.write_text(
        json.dumps(order, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def product_to_dict(product: Product) -> dict:
    return {
        "product_id": product.product_id,
        "name": product.name,
        "category": product.category,
        "price": product.price.amount,
        "currency": product.price.currency,
        "quantity": product.quantity,
    }


def export_catalog(products: list[Product], path: Path) -> None:
    """Атомарний експорт: запис у .tmp, потім os.replace."""
    tmp = path.with_suffix(path.suffix + ".tmp")
    payload = [product_to_dict(p) for p in products]
    try:
        tmp.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        os.replace(tmp, path)
    except BaseException:
        tmp.unlink(missing_ok=True)
        raise
