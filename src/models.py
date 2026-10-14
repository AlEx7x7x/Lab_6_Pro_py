from dataclasses import dataclass, field

from shop.value_objects import Money


@dataclass(frozen=True, slots=True)
class Product:
    product_id: int
    name: str
    price: Money
    category: str = "general"
    quantity: int = 0

    def __post_init__(self) -> None:
        if self.product_id <= 0:
            raise ValueError("Product id must be positive")
        if not self.name.strip():
            raise ValueError("Product name cannot be empty")
        if self.quantity < 0:
            raise ValueError("Quantity cannot be negative")

    @property
    def stock_value(self) -> Money:
        return Money(self.price.amount * self.quantity, self.price.currency)


@dataclass
class CartItem:
    product: Product
    quantity: int

    def __post_init__(self) -> None:
        if self.quantity <= 0:
            raise ValueError("Quantity must be positive")

    @property
    def total(self) -> Money:
        return Money(
            self.product.price.amount * self.quantity,
            self.product.price.currency,
        )


@dataclass
class Cart:
    items: list[CartItem] = field(default_factory=list)

    def add(self, product: Product, quantity: int = 1) -> None:
    # Валидация должна происходить до любых изменений
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        
        for item in self.items:
            if item.product.product_id == product.product_id:
                item.quantity += quantity
                return
        self.items.append(CartItem(product, quantity))

    def __len__(self) -> int:
        return len(self.items)

    def __contains__(self, product_id: int) -> bool:
        return any(i.product.product_id == product_id for i in self.items)

    @property
    def total(self) -> Money:
        if not self.items:
            return Money(0.0) # Порожній кошик коштує 0
    # Починаємо сумувати з першого елемента, що змусить Python викликати __add__ з класу Money
        return sum((i.total for i in self.items[1:]), start=self.items[0].total)
