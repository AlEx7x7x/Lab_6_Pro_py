import pytest

from shop.config import (
    DEFAULT_MIN_STOCK,
    get_min_stock,
    get_payment_mode,
    load_config,
)


def test_payment_mode_from_env(monkeypatch):
    monkeypatch.setenv("PAYMENT_MODE", "test")

    assert get_payment_mode() == "test"


def test_default_payment_mode(monkeypatch):
    monkeypatch.delenv("PAYMENT_MODE", raising=False)

    assert get_payment_mode() == "sandbox"


def test_min_stock_default(monkeypatch):
    monkeypatch.delenv("MIN_STOCK", raising=False)

    assert get_min_stock() == DEFAULT_MIN_STOCK


def test_min_stock_from_env(monkeypatch):
    monkeypatch.setenv("MIN_STOCK", "12")

    assert get_min_stock() == 12


def test_min_stock_zero_is_valid_boundary(monkeypatch):
    monkeypatch.setenv("MIN_STOCK", "0")

    assert get_min_stock() == 0


@pytest.mark.parametrize("raw", ["abc", "1.5", ""])
def test_min_stock_not_integer(monkeypatch, raw):
    monkeypatch.setenv("MIN_STOCK", raw)

    with pytest.raises(ValueError, match="integer") as exc_info:
        get_min_stock()

    assert isinstance(exc_info.value.__cause__, ValueError)  # chaining


def test_min_stock_negative(monkeypatch):
    monkeypatch.setenv("MIN_STOCK", "-3")

    with pytest.raises(ValueError, match="negative"):
        get_min_stock()


def test_load_config_from_yaml(tmp_path):
    path = tmp_path / "config.yaml"
    path.write_text(
        "min_stock: 7\ncurrency: USD\ncategories: [electronics, books]\n",
        encoding="utf-8",
    )

    assert load_config(path) == {
        "min_stock": 7,
        "currency": "USD",
        "categories": ["electronics", "books"],
    }


def test_load_config_uses_defaults_for_empty_file(tmp_path):
    path = tmp_path / "empty.yaml"
    path.write_text("", encoding="utf-8")

    assert load_config(path) == {
        "min_stock": DEFAULT_MIN_STOCK,
        "currency": "UAH",
        "categories": [],
    }


def test_load_config_missing_file(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_config(tmp_path / "nope.yaml")


def test_monkeypatch_setattr_replaces_function(monkeypatch):
    import shop.config as config

    monkeypatch.setattr(config, "get_min_stock", lambda: 99)

    assert config.get_min_stock() == 99
