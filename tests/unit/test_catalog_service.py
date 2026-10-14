import pytest

from shop.exceptions import ShopError
from shop.repositories import ProductRepository
from shop.services import CatalogService


@pytest.fixture
def service(repository):
    return CatalogService(repository)


def test_filter_by_category(service):
    result = service.filter_by_category("electronics")

    assert {p.name for p in result} == {"Laptop", "Mouse"}


def test_filter_by_category_ignores_case_and_spaces(service):
    assert len(service.filter_by_category("  FURNITURE ")) == 1


def test_filter_by_unknown_category_returns_empty(service):
    assert service.filter_by_category("toys") == []


def test_total_stock_value(service):
    # 35000*10 + 1200*3 + 7500*0
    assert service.total_stock_value().amount == pytest.approx(353_600)


def test_total_stock_value_of_empty_catalog():
    assert CatalogService(ProductRepository()).total_stock_value().amount == 0


def test_most_expensive_product(service):
    assert service.most_expensive().name == "Laptop"


def test_most_expensive_in_empty_catalog_raises():
    with pytest.raises(ShopError, match="empty"):
        CatalogService(ProductRepository()).most_expensive()


@pytest.mark.parametrize(
    ("min_stock", "expected_ids"),
    [
        pytest.param(0, [], id="threshold-zero"),
        pytest.param(1, [3], id="only-out-of-stock"),
        pytest.param(3, [3], id="exactly-equal-is-not-low"),
        pytest.param(4, [2, 3], id="mouse-becomes-low"),
        pytest.param(11, [1, 2, 3], id="everything-low"),
    ],
)
def test_low_stock_boundaries(service, min_stock, expected_ids):
    ids = sorted(p.product_id for p in service.low_stock(min_stock))

    assert ids == expected_ids
