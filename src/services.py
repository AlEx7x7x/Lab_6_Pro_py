from shop.exceptions import ShopError
from shop.models import Cart, Product
from shop.protocols import AsyncStockProvider, Notifier, PaymentGateway
from shop.repositories import ProductRepository
from shop.value_objects import Money


class PercentageDiscount:
    def __init__(self, percent: float) -> None:
        if not (0 <= percent <= 100):
            raise ValueError("Invalid discount")
        self.percent = percent

    def apply(self, total: Money) -> Money:
        return Money(total.amount * (1 - self.percent / 100), total.currency)


class CheckoutService:
    def __init__(
        self,
        payment_gateway: PaymentGateway,
        notifier: Notifier,
    ) -> None:
        self._gateway = payment_gateway
        self._notifier = notifier

    def checkout(self, email: str, cart: Cart) -> str:
        if len(cart) == 0:
            raise ValueError("Cart is empty")
        payment_id = self._gateway.pay(cart.total)
        self._notifier.send(email, f"Payment successful: {payment_id}")
        return payment_id


class CatalogService:
    """Бізнес-логіка каталогу над ProductRepository."""

    def __init__(self, repository: ProductRepository) -> None:
        self._repo = repository

    def filter_by_category(self, category: str) -> list[Product]:
        wanted = category.strip().lower()
        return [
            p for p in self._repo.list_all() if p.category.lower() == wanted
        ]

    def total_stock_value(self) -> Money:
        return Money(sum(p.stock_value.amount for p in self._repo.list_all()))

    def most_expensive(self) -> Product:
        products = self._repo.list_all()
        if not products:
            raise ShopError("Catalog is empty")
        return max(products, key=lambda p: p.price.amount)

    def low_stock(self, min_stock: int) -> list[Product]:
        return [p for p in self._repo.list_all() if p.quantity < min_stock]


class AsyncStockService:
    def __init__(self, provider: AsyncStockProvider) -> None:
        self._provider = provider

    async def available_quantity(self, product_id: int) -> int:
        data = await self._provider.fetch_stock(product_id)
        return int(data["quantity"])
