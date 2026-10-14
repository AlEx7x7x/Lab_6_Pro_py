import logging
from pathlib import Path

from reliable_importer.config import load_config
from reliable_importer.context import logged_operation
from reliable_importer.exceptions import ApplicationError
from reliable_importer.exporters import export_products_json
from reliable_importer.logging_config import configure_logging
from reliable_importer.services import ImportStatistics, import_products

logger = logging.getLogger(__name__)


def main() -> int:
    try:
        # Шляхи у конфігурації трактуються від кореня проєкту.
        root = Path.cwd()
        config = load_config(root / "config.yaml")
        configure_logging(config.log_level, root / config.log_path)
        stats = ImportStatistics()

        with logged_operation("Імпорт та експорт товарів"):
            products = import_products(
                root / config.input_path,
                mode=config.mode,
                minimum_stock=config.minimum_stock,
                allowed_categories=config.allowed_categories,
                stats=stats,
            )
            exported = export_products_json(products, root / config.output_path)

        logger.info(
            "Підсумок: усього=%d, коректних=%d, некоректних=%d, малий_залишок=%d, експортовано=%d",
            stats.total, stats.valid, stats.invalid, stats.low_stock, exported
        )
        print(f"Готово. Перевірте файл: {root / config.output_path}")
        print(f"Усього: {stats.total}; коректних: {stats.valid}; "
              f"некоректних: {stats.invalid}; експортовано: {exported}")
        return 0
    except ApplicationError as error:
        logging.getLogger(__name__).error("Критична помилка застосунку: %s", error)
        print(f"Помилка: {error}")
        return 1
    except OSError as error:
        logging.getLogger(__name__).exception("Критична помилка файлової системи")
        print(f"Помилка файлової системи: {error}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
