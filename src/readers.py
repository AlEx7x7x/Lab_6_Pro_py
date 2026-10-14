import csv
from collections.abc import Iterator
from pathlib import Path

from reliable_importer.exceptions import DataImportError


def read_csv_rows(path: Path) -> Iterator[tuple[int, dict[str, str]]]:
    """Потоково повертає (номер рядка, словник полів), не накопичуючи весь CSV."""
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as stream:
            reader = csv.DictReader(stream)
            required = {"product_id", "name", "category", "price", "quantity"}
            if reader.fieldnames is None or not required.issubset(set(reader.fieldnames)):
                raise DataImportError(
                    "CSV повинен містити колонки: product_id,name,category,price,quantity"
                )
            for line_number, row in enumerate(reader, start=2):
                yield line_number, row
    except OSError as error:
        raise DataImportError(f"Не вдалося прочитати CSV: {path}") from error
