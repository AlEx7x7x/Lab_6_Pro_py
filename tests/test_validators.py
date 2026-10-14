import pytest
from reliable_importer.exceptions import RecordValidationError
from reliable_importer.validators import parse_product


CATEGORIES = ("Electronics", "Books")


def test_valid_product():
    product = parse_product(
        {"product_id": "1", "name": "Book", "category": "Books",
         "price": "10.5", "quantity": "3"},
        line_number=2, allowed_categories=CATEGORIES
    )
    assert product.product_id == 1
    assert product.price == 10.5


def test_negative_price_is_rejected():
    with pytest.raises(RecordValidationError):
        parse_product(
            {"product_id": "1", "name": "Book", "category": "Books",
             "price": "-1", "quantity": "3"},
            line_number=2, allowed_categories=CATEGORIES
        )
