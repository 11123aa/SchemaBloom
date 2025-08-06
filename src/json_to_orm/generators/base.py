"""
Базовый генератор моделей.

Этот модуль содержит абстрактный базовый класс для генераторов
ORM моделей различных фреймворков.
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, List, Optional

from jinja2 import Environment, FileSystemLoader

from ..utils.logger import get_logger
from ..utils.template_filters import FILTERS

logger = get_logger(__name__)


class BaseGenerator(ABC):
    """
    Абстрактный базовый класс для генераторов ORM моделей.

    Этот класс определяет интерфейс для генераторов моделей
    различных ORM фреймворков (Prisma, Django, SQLAlchemy).
    """

    def __init__(self) -> None:
        """Инициализация генератора."""
        self.logger = logger
        self._setup_template_engine()

    def _setup_template_engine(self) -> None:
        """Настройка движка шаблонов Jinja2."""
        template_dir = Path(__file__).parent.parent / "templates"
        self.template_engine = Environment(
            loader=FileSystemLoader(str(template_dir)),
            trim_blocks=True,
            lstrip_blocks=True,
            keep_trailing_newline=True
        )
        
        # Регистрируем фильтры
        for name, filter_func in FILTERS.items():
            self.template_engine.filters[name] = filter_func

    @abstractmethod
    def generate_models(
        self, schema_data: Dict[str, Any], output_dir: str
    ) -> List[str]:
        """
        Генерирует модели на основе схемы данных.

        Args:
            schema_data: Данные схемы
            output_dir: Директория для сохранения файлов

        Returns:
            Список путей к созданным файлам
        """
        pass

    @abstractmethod
    def get_supported_types(self) -> Dict[str, str]:
        """
        Возвращает словарь поддерживаемых типов данных.

        Returns:
            Словарь {тип_схемы: тип_orm}
        """
        pass

    @abstractmethod
    def get_file_extension(self) -> str:
        """
        Возвращает расширение файла для данного формата.

        Returns:
            Расширение файла (например, '.py', '.prisma')
        """
        pass

    def validate_schema(self, schema_data: Dict[str, Any]) -> bool:
        """
        Валидирует схему данных для данного генератора.

        Args:
            schema_data: Данные схемы

        Returns:
            True если схема валидна для данного генератора
        """
        # Базовая валидация - проверяем наличие таблиц
        if "tables" not in schema_data:
            self.logger.error("Схема не содержит таблиц")
            return False

        tables = schema_data["tables"]
        if not isinstance(tables, list):
            self.logger.error("Поле 'tables' должно быть массивом")
            return False

        if not tables:
            self.logger.warning("Схема не содержит таблиц")
            return True

        # Проверяем типы данных в таблицах
        supported_types = self.get_supported_types()

        for table in tables:
            if not isinstance(table, dict):
                self.logger.error("Таблица должна быть объектом")
                return False

            if "name" not in table:
                self.logger.error("Таблица не имеет поля 'name'")
                return False

            fields = table.get("fields", [])
            for field in fields:
                if not isinstance(field, dict):
                    self.logger.error("Поле должно быть объектом")
                    return False

                if "type" not in field:
                    self.logger.error("Поле не имеет типа")
                    return False

                field_type = field["type"]
                if field_type not in supported_types:
                    self.logger.warning(
                        f"Тип '{field_type}' не поддерживается в {self.__class__.__name__}"
                    )

        return True

    def create_output_directory(self, output_dir: str) -> Path:
        """
        Создает выходную директорию если она не существует.

        Args:
            output_dir: Путь к директории

        Returns:
            Path объект директории
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        self.logger.info(f"Создана директория: {output_path}")
        return output_path

    def write_file(self, file_path: Path, content: str) -> None:
        """
        Записывает содержимое в файл.

        Args:
            file_path: Путь к файлу
            content: Содержимое для записи
        """
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            self.logger.info(f"Создан файл: {file_path}")
        except Exception as e:
            self.logger.error(f"Ошибка при создании файла {file_path}: {e}")
            raise

    def get_table_name(self, table: Dict[str, Any]) -> str:
        """
        Извлекает имя таблицы.

        Args:
            table: Данные таблицы

        Returns:
            Имя таблицы
        """
        return table.get("name", "unknown_table")

    def get_field_name(self, field: Dict[str, Any]) -> str:
        """
        Извлекает имя поля.

        Args:
            field: Данные поля

        Returns:
            Имя поля
        """
        return field.get("name", "unknown_field")

    def get_field_type(self, field: Dict[str, Any]) -> str:
        """
        Извлекает тип поля.

        Args:
            field: Данные поля

        Returns:
            Тип поля
        """
        return field.get("type", "string")

    def is_primary_key(self, field: Dict[str, Any]) -> bool:
        """
        Проверяет, является ли поле первичным ключом.

        Args:
            field: Данные поля

        Returns:
            True если поле является первичным ключом
        """
        return field.get("primary_key", False)

    def is_nullable(self, field: Dict[str, Any]) -> bool:
        """
        Проверяет, может ли поле быть null.

        Args:
            field: Данные поля

        Returns:
            True если поле может быть null
        """
        return field.get("nullable", True)

    def is_unique(self, field: Dict[str, Any]) -> bool:
        """
        Проверяет, является ли поле уникальным.

        Args:
            field: Данные поля

        Returns:
            True если поле уникальное
        """
        return field.get("unique", False)

    def get_default_value(self, field: Dict[str, Any]) -> Optional[str]:
        """
        Извлекает значение по умолчанию для поля.

        Args:
            field: Данные поля

        Returns:
            Значение по умолчанию или None
        """
        return field.get("default")

    def get_relationships_for_table(
        self, table_name: str, relationships: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Получает связи для конкретной таблицы.

        Args:
            table_name: Имя таблицы
            relationships: Список всех связей

        Returns:
            Список связей для таблицы
        """
        table_relationships = []

        for rel in relationships:
            if rel.get("from") == table_name or rel.get("to") == table_name:
                table_relationships.append(rel)

        return table_relationships
