import pytest

from shop.value_objects import Money


def test_money_creation():
    money = Money(100, "UAH")

    assert money.amount == 100
    assert money.currency == "UAH"


def test_default_currency_is_uah():
    assert Money(1).currency == "UAH"


def test_negative_money_rejected():
    with pytest.raises(ValueError, match="negative"):
        Money(-1, "UAH")


def test_money_addition():
    assert Money(100) + Money(50) == Money(150)


def test_currency_mismatch():
    with pytest.raises(ValueError, match="Currency"):
        Money(100, "UAH") + Money(10, "USD")


@pytest.mark.parametrize(
    ("amount", "expected"),
    [
        pytest.param(0, 0, id="minimum"),
        pytest.param(0.01, 0.01, id="just-above-minimum"),
        pytest.param(100, 100, id="normal"),
        pytest.param(9999.99, 9999.99, id="large"),
    ],
)
def test_valid_money_amounts(amount, expected):
    assert Money(amount).amount == pytest.approx(expected)


def test_float_addition_uses_approx():
    result = Money(0.1) + Money(0.2)

    assert result.amount != 0.3  # типова пастка floating-point
    assert result.amount == pytest.approx(0.3)
