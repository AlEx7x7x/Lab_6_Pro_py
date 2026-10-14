import pytest

from shop.exceptions import DataImportError
from shop.importers import read_products


def test_csv_import(csv_file):
    result = list(read_products(csv_file))

    assert len(result) == 3
    assert result[0].name == "Laptop"
    assert result[0].price.amount == pytest.approx(35_000)


def test_csv_import_is_lazy(csv_file):
    generator = read_products(csv_file)

    assert next(generator).product_id == 1  # потоково, без повного читання


def test_header_only_file_gives_no_products(tmp_path):
    path = tmp_path / "empty.csv"
    path.write_text("product_id,name,category,price,quantity\n", encoding="utf-8")

    assert list(read_products(path)) == []


def test_missing_column_rejected(tmp_path):
    path = tmp_path / "bad.csv"
    path.write_text("product_id,name\n1,Laptop\n", encoding="utf-8")

    with pytest.raises(DataImportError, match="Missing columns"):
        list(read_products(path))


@pytest.mark.parametrize(
    ("row", "line"),
    [
        pytest.param("x,Laptop,electronics,100,1", 2, id="bad-id"),
        pytest.param("1,Laptop,electronics,cheap,1", 2, id="bad-price"),
        pytest.param("1,Laptop,electronics,-5,1", 2, id="negative-price"),
        pytest.param("1,Laptop,electronics,100,-1", 2, id="negative-quantity"),
        pytest.param("1,Laptop,electronics,100,1.5", 2, id="float-quantity"),
        pytest.param("1,,electronics,100,1", 2, id="empty-name"),
    ],
)
def test_malformed_record(tmp_path, row, line):
    path = tmp_path / "bad.csv"
    path.write_text(
        "product_id,name,category,price,quantity\n" + row + "\n",
        encoding="utf-8",
    )

    with pytest.raises(DataImportError) as exc_info:
        list(read_products(path))

    assert exc_info.value.line == line
    assert isinstance(exc_info.value.__cause__, ValueError)


def test_short_row_reports_line_number(tmp_path):
    path = tmp_path / "short.csv"
    path.write_text(
        "product_id,name,category,price,quantity\n1,Laptop\n",
        encoding="utf-8",
    )

    with pytest.raises(DataImportError) as exc_info:
        list(read_products(path))

    assert exc_info.value.line == 2


def test_import_missing_file(tmp_path):
    with pytest.raises(FileNotFoundError):
        list(read_products(tmp_path / "absent.csv"))
