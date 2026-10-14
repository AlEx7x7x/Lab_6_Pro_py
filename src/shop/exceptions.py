"""Власні винятки застосунку."""


class ShopError(Exception):
    """Базовий виняток предметної області."""


class PaymentError(ShopError):
    """Платіжний шлюз недоступний або відхилив операцію."""


class DataImportError(ShopError):
    """Некоректний запис під час імпорту CSV."""

    def __init__(self, message: str, line: int | None = None) -> None:
        super().__init__(message)
        self.line = line


class ProductNotFoundError(ShopError):
    """Товар не знайдено в каталозі."""


class DuplicateProductError(ShopError):
    """Товар із таким ID уже існує в каталозі."""
