from reliable_importer.exceptions import RecordValidationError
from reliable_importer.models import Product


def parse_product(row: dict[str, str], *, line_number: int,
                  allowed_categories: tuple[str, ...]) -> Product:
    def invalid(message: str, field: str) -> RecordValidationError:
        return RecordValidationError(message, line_number=line_number, field=field)

    try:
        product_id = int(row["product_id"])
    except (KeyError, TypeError, ValueError) as error:
        raise invalid("product_id має бути цілим числом", "product_id") from error
    if product_id <= 0:
        raise invalid("product_id має бути більшим за нуль", "product_id")

    name = (row.get("name") or "").strip()
    if not name:
        raise invalid("Назва товару не може бути порожньою", "name")

    category = (row.get("category") or "").strip()
    if category not in allowed_categories:
        raise invalid(f"Недозволена категорія: {category!r}", "category")

    try:
        price = float(row["price"])
    except (KeyError, TypeError, ValueError) as error:
        raise invalid("price має бути числом", "price") from error
    if price < 0:
        raise invalid("price не може бути від'ємною", "price")

    try:
        quantity = int(row["quantity"])
    except (KeyError, TypeError, ValueError) as error:
        raise invalid("quantity має бути цілим числом", "quantity") from error
    if quantity < 0:
        raise invalid("quantity не може бути від'ємною", "quantity")

    return Product(product_id, name, category, price, quantity)
