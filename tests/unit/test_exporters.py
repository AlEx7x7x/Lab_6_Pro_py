import json

import pytest

from shop.exporters import export_catalog, export_order, product_to_dict


def test_export_order(tmp_path):
    output = tmp_path / "order.json"
    order = {"id": 1, "total": 100.0, "status": "paid"}

    export_order(order, output)

    assert output.exists()
    assert json.loads(output.read_text(encoding="utf-8")) == order


def test_export_order_keeps_cyrillic(tmp_path):
    output = tmp_path / "order.json"

    export_order({"customer": "Анна"}, output)

    assert "Анна" in output.read_text(encoding="utf-8")


def test_product_to_dict(laptop):
    assert product_to_dict(laptop) == {
        "product_id": 1,
        "name": "Laptop",
        "category": "electronics",
        "price": 35_000,
        "currency": "UAH",
        "quantity": 10,
    }


def test_export_empty_catalog(tmp_path):
    output = tmp_path / "catalog.json"

    export_catalog([], output)

    assert json.loads(output.read_text(encoding="utf-8")) == []


def test_atomic_export_keeps_old_data_on_failure(tmp_path, laptop, monkeypatch):
    output = tmp_path / "catalog.json"
    output.write_text("old valid data", encoding="utf-8")

    def broken_replace(src, dst):
        raise OSError("disk error")

    monkeypatch.setattr("shop.exporters.os.replace", broken_replace)

    with pytest.raises(OSError, match="disk error"):
        export_catalog([laptop], output)

    assert output.read_text(encoding="utf-8") == "old valid data"
    assert not output.with_suffix(".json.tmp").exists()
