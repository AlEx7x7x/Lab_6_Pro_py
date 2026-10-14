from collections.abc import Iterable

from shop.exceptions import DuplicateProductError, ProductNotFoundError
from shop.models import Product


class ProductRepository:
    """Каталог товарів у пам'яті."""

    def __init__(self) -> None:
        self._items: dict[int, Product] = {}

    def add(self, product: Product) -> None:
        if product.product_id in self._items:
            raise DuplicateProductError(
                f"Product {product.product_id} already exists"
            )
        self._items[product.product_id] = product

    def add_many(self, products: Iterable[Product]) -> int:
        count = 0
        for product in products:
            self.add(product)
            count += 1
        return count

    def get(self, product_id: int) -> Product:
        try:
            return self._items[product_id]
        except KeyError:
            raise ProductNotFoundError(
                f"Product {product_id} not found"
            ) from None

    def find_by_name(self, name: str) -> list[Product]:
        needle = name.strip().lower()
        return [p for p in self._items.values() if needle in p.name.lower()]

    def list_all(self) -> list[Product]:
        return list(self._items.values())

    def __len__(self) -> int:
        return len(self._items)
