import pytest

from shop.exceptions import DuplicateProductError, ProductNotFoundError
from shop.repositories import ProductRepository


def test_add_and_get_product(repository):
    assert repository.get(1).name == "Laptop"
    assert len(repository) == 3


def test_get_missing_product_raises_custom_exception(repository):
    with pytest.raises(ProductNotFoundError) as exc_info:
        repository.get(999)

    assert "999" in str(exc_info.value)


def test_duplicate_product_rejected(repository, product_factory):
    with pytest.raises(DuplicateProductError, match="already exists"):
        repository.add(product_factory(product_id=1))

    assert len(repository) == 3


def test_find_by_name_is_case_insensitive(repository):
    found = repository.find_by_name("  LAP ")

    assert [p.product_id for p in found] == [1]


def test_find_by_name_no_match(repository):
    assert repository.find_by_name("phone") == []


def test_add_many_returns_count(product_factory):
    repo = ProductRepository()

    added = repo.add_many(
        product_factory(product_id=i, name=f"P{i}") for i in (1, 2, 3)
    )

    assert added == 3
    assert len(repo) == 3


def test_repository_methods_with_fake_collaborator_state(product_factory):
    """Fake замість Mock: перевіряємо стан, а не виклики."""
    repo = ProductRepository()
    repo.add(product_factory(product_id=7, name="Cable"))

    assert repo.get(7).name == "Cable"
    assert repo.list_all()[0].product_id == 7
