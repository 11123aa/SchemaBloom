"""
Валидатор схем данных.

Этот модуль содержит классы для валидации JSON-схем данных,
используемых для генерации ORM моделей.
"""

from typing import Any, Dict, List, Optional, Tuple

from ..utils.logger import get_logger

logger = get_logger(__name__)


class SchemaValidator:
    """
    Валидатор схем данных.

    Этот класс отвечает за валидацию JSON-схем данных,
    проверяя корректность структуры, типов данных и связей.
    """

    def __init__(self) -> None:
        """Инициализация валидатора."""
        self.logger = logger
        self.errors: List[str] = []
        self.warnings: List[str] = []

    def validate_schema(
        self, data: Dict[str, Any]
    ) -> Tuple[bool, List[str], List[str]]:
        """
        Валидирует полную схему данных.

        Args:
            data: Данные схемы для валидации

        Returns:
            Кортеж (is_valid, errors, warnings)
        """
        self.errors = []
        self.warnings = []

        # Базовая валидация структуры
        if not self._validate_structure(data):
            return False, self.errors, self.warnings

        # Валидация таблиц
        tables = data.get("tables", [])
        if not self._validate_tables(tables):
            return False, self.errors, self.warnings

        # Валидация связей
        relationships = data.get("relationships", [])
        if not self._validate_relationships(relationships, tables):
            return False, self.errors, self.warnings

        is_valid = len(self.errors) == 0
        return is_valid, self.errors, self.warnings

    def _validate_structure(self, data: Dict[str, Any]) -> bool:
        """
        Валидирует базовую структуру схемы.

        Args:
            data: Данные схемы

        Returns:
            True если структура корректна
        """
        if not isinstance(data, dict):
            self.errors.append("Схема должна быть объектом (словарем)")
            return False

        # Проверяем обязательные поля
        required_fields = ["tables"]
        for field in required_fields:
            if field not in data:
                self.errors.append(f"Отсутствует обязательное поле: {field}")
                return False

        # Проверяем типы полей
        if not isinstance(data["tables"], list):
            self.errors.append("Поле 'tables' должно быть массивом")
            return False

        if "relationships" in data and not isinstance(data["relationships"], list):
            self.errors.append("Поле 'relationships' должно быть массивом")
            return False

        return True

    def _validate_tables(self, tables: List[Dict[str, Any]]) -> bool:
        """
        Валидирует список таблиц.

        Args:
            tables: Список таблиц

        Returns:
            True если все таблицы корректны
        """
        if not tables:
            self.warnings.append("Схема не содержит таблиц")
            return True

        table_names = set()

        for i, table in enumerate(tables):
            if not isinstance(table, dict):
                self.errors.append(f"Таблица {i} должна быть объектом")
                continue

            # Проверяем обязательные поля таблицы
            if "name" not in table:
                self.errors.append(f"Таблица {i} не имеет поля 'name'")
                continue

            table_name = table["name"]
            if not isinstance(table_name, str):
                self.errors.append(f"Имя таблицы {i} должно быть строкой")
                continue

            if table_name in table_names:
                self.errors.append(f"Дублирующееся имя таблицы: {table_name}")
                continue

            table_names.add(table_name)

            # Валидируем поля таблицы
            fields = table.get("fields", [])
            if not self._validate_fields(fields, table_name):
                continue

        return len(self.errors) == 0

    def _validate_fields(self, fields: List[Dict[str, Any]], table_name: str) -> bool:
        """
        Валидирует поля таблицы.

        Args:
            fields: Список полей
            table_name: Имя таблицы

        Returns:
            True если все поля корректны
        """
        if not isinstance(fields, list):
            self.errors.append(f"Поля таблицы '{table_name}' должны быть массивом")
            return False

        if not fields:
            self.warnings.append(f"Таблица '{table_name}' не содержит полей")

        field_names = set()

        for i, field in enumerate(fields):
            if not isinstance(field, dict):
                self.errors.append(
                    f"Поле {i} таблицы '{table_name}' должно быть объектом"
                )
                continue

            # Проверяем обязательные поля
            if "name" not in field:
                self.errors.append(
                    f"Поле {i} таблицы '{table_name}' не имеет поля 'name'"
                )
                continue

            if "type" not in field:
                self.errors.append(
                    f"Поле {i} таблицы '{table_name}' не имеет поля 'type'"
                )
                continue

            field_name = field["name"]
            field_type = field["type"]

            if not isinstance(field_name, str):
                self.errors.append(
                    f"Имя поля {i} таблицы '{table_name}' должно быть строкой"
                )
                continue

            if not isinstance(field_type, str):
                self.errors.append(
                    f"Тип поля {i} таблицы '{table_name}' должен быть строкой"
                )
                continue

            if field_name in field_names:
                self.errors.append(
                    f"Дублирующееся имя поля '{field_name}' в таблице '{table_name}'"
                )
                continue

            field_names.add(field_name)

            # Валидируем тип поля
            if not self._validate_field_type(field_type, field, table_name, field_name):
                continue

        return len(self.errors) == 0

    def _validate_field_type(
        self, field_type: str, field: Dict[str, Any], table_name: str, field_name: str
    ) -> bool:
        """
        Валидирует тип поля.

        Args:
            field_type: Тип поля
            field: Данные поля
            table_name: Имя таблицы
            field_name: Имя поля

        Returns:
            True если тип корректный
        """
        valid_types = {
            "string",
            "integer",
            "float",
            "boolean",
            "datetime",
            "date",
            "time",
            "text",
            "json",
            "binary",
        }

        if field_type not in valid_types:
            self.errors.append(
                f"Неизвестный тип '{field_type}' для поля '{field_name}' в таблице '{table_name}'. "
                f"Допустимые типы: {', '.join(sorted(valid_types))}"
            )
            return False

        return True

    def _validate_relationships(
        self, relationships: List[Dict[str, Any]], tables: List[Dict[str, Any]]
    ) -> bool:
        """
        Валидирует связи между таблицами.

        Args:
            relationships: Список связей
            tables: Список таблиц

        Returns:
            True если все связи корректны
        """
        if not relationships:
            return True

        table_names = {table["name"] for table in tables if "name" in table}

        for i, relationship in enumerate(relationships):
            if not isinstance(relationship, dict):
                self.errors.append(f"Связь {i} должна быть объектом")
                continue

            # Проверяем обязательные поля связи
            required_fields = ["from", "to", "type"]
            for field in required_fields:
                if field not in relationship:
                    self.errors.append(f"Связь {i} не имеет поля '{field}'")
                    continue

            from_table = relationship["from"]
            to_table = relationship["to"]
            rel_type = relationship["type"]

            # Проверяем существование таблиц
            if from_table not in table_names:
                self.errors.append(
                    f"Связь {i} ссылается на несуществующую таблицу: {from_table}"
                )
                continue

            if to_table not in table_names:
                self.errors.append(
                    f"Связь {i} ссылается на несуществующую таблицу: {to_table}"
                )
                continue

            # Проверяем тип связи
            valid_types = {"one_to_one", "one_to_many", "many_to_one", "many_to_many"}
            if rel_type not in valid_types:
                self.errors.append(
                    f"Неизвестный тип связи '{rel_type}' в связи {i}. "
                    f"Допустимые типы: {', '.join(sorted(valid_types))}"
                )
                continue

        return len(self.errors) == 0
