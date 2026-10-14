import pytest

from shop.services import PercentageDiscount
from shop.value_objects import Money


@pytest.mark.parametrize(
    ("percent", "expected"),
    [(0, 100), (10, 90), (25, 75), (50, 50), (100, 0)],
)
def test_percentage_discount(percent, expected):
    result = PercentageDiscount(percent).apply(Money(100))

    assert result.amount == pytest.approx(expected)


@pytest.mark.parametrize("percent", [-1, -0.01, 100.01, 150])
def test_invalid_discount(percent):
    with pytest.raises(ValueError, match="Invalid discount"):
        PercentageDiscount(percent)


def test_discount_keeps_currency():
    result = PercentageDiscount(10).apply(Money(200, "USD"))

    assert result.currency == "USD"
