# shop_project — Лабораторна робота №6 (Варіант 3: Інтернет-магазин)

Автоматизоване тестування Python-програми за допомогою pytest.

## Встановлення

```bash
python -m pip install -e ".[dev]"
```

## Запуск (рекомендована команда з методички)

```bash
pytest -v --cov=shop --cov-branch --cov-report=term-missing --cov-report=html
```

* лише unit: `pytest -m "not integration"`
* лише integration: `pytest -m integration`
* один файл: `pytest tests/unit/test_checkout.py -v`
* один тест: `pytest tests/unit/test_checkout.py::test_checkout_success -v`

HTML-звіт coverage: `htmlcov/index.html`.
