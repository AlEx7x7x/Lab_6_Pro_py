import json

import pytest

from shop.exceptions import DataImportError
from shop.exporters import export_catalog
from shop.importers import read_products
from shop.repositories import ProductRepository
from shop.services import CatalogService


@pytest.mark.integration
def test_import_processing_export_pipeline(csv_file, tmp_path):
    repo = ProductRepository()
    repo.add_many(read_products(csv_file))
    service = CatalogService(repo)
    output = tmp_path / "electronics.json"

    export_catalog(service.filter_by_category("electronics"), output)

    data = json.loads(output.read_text(encoding="utf-8"))
    assert [item["name"] for item in data] == ["Laptop", "Mouse"]
    assert service.total_stock_value().amount == pytest.approx(353_600)
    assert service.most_expensive().name == "Laptop"


@pytest.mark.integration
def test_malformed_csv_stops_pipeline_without_output(tmp_path):
    source = tmp_path / "broken.csv"
    source.write_text(
        "product_id,name,category,price,quantity\n"
        "1,Laptop,electronics,35000,10\n"
        "2,Mouse,electronics,oops,3\n",
        encoding="utf-8",
    )
    repo = ProductRepository()
    output = tmp_path / "catalog.json"

    with pytest.raises(DataImportError) as exc_info:
        repo.add_many(read_products(source))
        export_catalog(repo.list_all(), output)

    assert exc_info.value.line == 3
    assert not output.exists()
    assert len(repo) == 1  # перший валідний запис уже імпортований
