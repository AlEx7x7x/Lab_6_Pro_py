import pytest

from shop.models import Cart, Product
from shop.repositories import ProductRepository
from shop.value_objects import Money


@pytest.fixture
def laptop() -> Product:
    return Product(
        product_id=1,
        name="Laptop",
        price=Money(35_000),
        category="electronics",
        quantity=10,
    )


@pytest.fixture
def mouse() -> Product:
    return Product(
        product_id=2,
        name="Mouse",
        price=Money(1_200),
        category="electronics",
        quantity=3,
    )


@pytest.fixture
def cart(laptop, mouse) -> Cart:
    cart = Cart()
    cart.add(laptop, 1)
    cart.add(mouse, 2)
    return cart


@pytest.fixture
def product_factory():
    """Fixture factory: створює Product із керованими параметрами."""

    def create_product(
        *,
        product_id: int = 1,
        name: str = "Product",
        price: float = 100,
        category: str = "general",
        quantity: int = 1,
    ) -> Product:
        return Product(
            product_id=product_id,
            name=name,
            price=Money(price),
            category=category,
            quantity=quantity,
        )

    return create_product


@pytest.fixture
def repository(product_factory):
    """Fixture із yield: setup -> тест -> teardown."""
    repo = ProductRepository()
    repo.add(product_factory(product_id=1, name="Laptop", price=35_000,
                             category="electronics", quantity=10))
    repo.add(product_factory(product_id=2, name="Mouse", price=1_200,
                             category="electronics", quantity=3))
    repo.add(product_factory(product_id=3, name="Desk", price=7_500,
                             category="furniture", quantity=0))
    yield repo
    repo._items.clear()  # teardown: каталог очищується після кожного тесту


@pytest.fixture
def csv_file(tmp_path):
    path = tmp_path / "products.csv"
    path.write_text(
        "product_id,name,category,price,quantity\n"
        "1,Laptop,electronics,35000,10\n"
        "2,Mouse,electronics,1200,3\n"
        "3,Desk,furniture,7500,0\n",
        encoding="utf-8",
    )
    return path
