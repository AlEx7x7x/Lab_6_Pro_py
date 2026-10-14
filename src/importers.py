import csv
from collections.abc import Iterator
from pathlib import Path

from shop.exceptions import DataImportError
from shop.models import Product
from shop.value_objects import Money

REQUIRED_COLUMNS = ("product_id", "name", "category", "price", "quantity")


def read_products(path: Path) -> Iterator[Product]:
    """Потоково читає CSV та віддає валідні Product.

    Некоректний запис -> DataImportError з номером рядка та __cause__.
    """
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        missing = [c for c in REQUIRED_COLUMNS if c not in (reader.fieldnames or [])]
        if missing:
            raise DataImportError(f"Missing columns: {', '.join(missing)}")
        for row in reader:
            line = reader.line_num
            try:
                currency = row.get("currency", "UAH")
                yield Product(
                    product_id=int(row["product_id"]),
                    name=row["name"],
                    category=row["category"],
                    price=Money(float(row["price"]), currency), # Обязательно передаем валюту!
                    quantity=int(row["quantity"]),
                )   
            except (ValueError, TypeError) as error:
                raise DataImportError(
                    f"Invalid record at line {line}: {error}", line=line
                ) from error
