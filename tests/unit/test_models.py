import pytest

from shop.models import Cart, CartItem, Product
from shop.value_objects import Money


def test_product_creation(laptop):
    assert laptop.name == "Laptop"
    assert laptop.price.amount == 35_000
    assert laptop.category == "electronics"


def test_product_stock_value(laptop):
    assert laptop.stock_value.amount == pytest.approx(350_000)


@pytest.mark.parametrize(
    ("kwargs", "message"),
    [
        pytest.param({"product_id": 0}, "id", id="zero-id"),
        pytest.param({"product_id": -5}, "id", id="negative-id"),
        pytest.param({"name": ""}, "name", id="empty-name"),
        pytest.param({"name": "   "}, "name", id="blank-name"),
        pytest.param({"quantity": -1}, "Quantity", id="negative-quantity"),
    ],
)
def test_invalid_product_fields(kwargs, message):
    base = {"product_id": 1, "name": "X", "price": Money(10)}

    with pytest.raises(ValueError, match=message):
        Product(**{**base, **kwargs})


def test_product_zero_quantity_is_boundary_valid():
    product = Product(1, "X", Money(10), quantity=0)

    assert product.stock_value.amount == 0


def test_empty_cart():
    cart = Cart()

    assert len(cart) == 0
    assert cart.total.amount == 0


def test_cart_length(cart):
    assert len(cart) == 2


def test_cart_contains_product(cart):
    assert 1 in cart
    assert 2 in cart
    assert 999 not in cart


def test_cart_total(cart):
    assert cart.total.amount == pytest.approx(37_400)


@pytest.mark.parametrize("quantity", [0, -1, -100])
def test_invalid_cart_quantity(laptop, quantity):
    cart = Cart()

    with pytest.raises(ValueError, match="positive"):
        cart.add(laptop, quantity)

    assert len(cart) == 0  # некоректна позиція не потрапила в кошик


def test_cart_item_total(mouse):
    assert CartItem(mouse, 3).total.amount == pytest.approx(3_600)
