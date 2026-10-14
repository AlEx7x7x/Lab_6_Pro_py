import json

import pytest

from shop.config import get_min_stock, load_config
from shop.exporters import export_catalog
from shop.importers import read_products
from shop.repositories import ProductRepository
from shop.services import CatalogService


@pytest.mark.integration
def test_low_stock_report_uses_env_configuration(monkeypatch, csv_file, tmp_path):
    monkeypatch.setenv("MIN_STOCK", "4")
    repo = ProductRepository()
    repo.add_many(read_products(csv_file))
    low = CatalogService(repo).low_stock(get_min_stock())
    output = tmp_path / "low_stock.json"

    export_catalog(low, output)

    names = [item["name"] for item in json.loads(output.read_text("utf-8"))]
    assert names == ["Mouse", "Desk"]


@pytest.mark.integration
def test_low_stock_report_uses_yaml_configuration(csv_file, tmp_path):
    config_path = tmp_path / "config.yaml"
    config_path.write_text("min_stock: 1\n", encoding="utf-8")
    config = load_config(config_path)
    repo = ProductRepository()
    repo.add_many(read_products(csv_file))

    low = CatalogService(repo).low_stock(config["min_stock"])

    assert [p.name for p in low] == ["Desk"]
