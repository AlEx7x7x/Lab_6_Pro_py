from typing import Protocol

from shop.value_objects import Money


class PaymentGateway(Protocol):
    def pay(self, amount: Money) -> str: ...


class Notifier(Protocol):
    def send(self, recipient: str, message: str) -> None: ...


class AsyncStockProvider(Protocol):
    async def fetch_stock(self, product_id: int) -> dict: ...
