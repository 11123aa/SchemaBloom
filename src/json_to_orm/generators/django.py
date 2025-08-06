"""
Генератор Django моделей.

Этот модуль содержит генератор для создания Django моделей
на основе JSON-схем данных.
"""

from pathlib import Path
from typing import Any, Dict, List

from .base import BaseGenerator


class DjangoGenerator(BaseGenerator):
    """
    Генератор Django моделей.

    Этот класс генерирует Django модели на основе JSON-схем данных.
    """

    def __init__(self) -> None:
        """Инициализация Django генератора."""
        super().__init__()

    def generate_models(
        self, schema_data: Dict[str, Any], output_dir: str
    ) -> List[str]:
        """
        Генерирует Django модели на основе схемы данных.

        Args:
            schema_data: Данные схемы
            output_dir: Директория для сохранения файлов

        Returns:
            Список путей к созданным файлов
        """
        if not self.validate_schema(schema_data):
            self.logger.error("Схема данных невалидна для Django генератора")
            return []

        # Создаем выходную директорию
        output_path = self.create_output_directory(output_dir)
        
        # Подготавливаем данные для шаблона
        tables = schema_data.get("tables", [])
        processed_tables = []
        
        for table in tables:
            processed_table = self._process_table(table, schema_data.get("relationships", []))
            processed_tables.append(processed_table)
        
        # Рендерим шаблон моделей
        template = self.template_engine.get_template("django/models.py.j2")
        content = template.render(tables=processed_tables)
        
        # Сохраняем файл
        file_path = output_path / f"models{self.get_file_extension()}"
        self.write_file(file_path, content)
        
        self.logger.info(f"Создан файл Django моделей: {file_path}")
        return [str(file_path)]

    def _process_table(self, table: Dict[str, Any], relationships: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Обрабатывает таблицу для шаблона.
        
        Args:
            table: Данные таблицы
            relationships: Список связей
            
        Returns:
            Обработанная таблица
        """
        processed_table = {
            "name": self.get_table_name(table),
            "fields": [],
            "relationships": []
        }
        
        # Обрабатываем поля
        for field in table.get("fields", []):
            processed_field = {
                "name": self.get_field_name(field),
                "type": self.get_field_type(field),
                "is_primary_key": self.is_primary_key(field),
                "is_unique": self.is_unique(field),
                "is_nullable": self.is_nullable(field),
                "default_value": self.get_default_value(field),
                "max_length": field.get("max_length"),
                "choices": field.get("choices"),
                "help_text": field.get("help_text"),
                "verbose_name": field.get("verbose_name"),
                "relation": field.get("relation")
            }
            processed_table["fields"].append(processed_field)
        
        # Обрабатываем связи для этой таблицы
        table_relationships = self.get_relationships_for_table(
            processed_table["name"], relationships
        )
        processed_table["relationships"] = table_relationships
        
        return processed_table

    def get_supported_types(self) -> Dict[str, str]:
        """
        Возвращает словарь поддерживаемых типов данных Django.

        Returns:
            Словарь {тип_схемы: тип_django}
        """
        return {
            "string": "CharField",
            "integer": "IntegerField",
            "float": "FloatField",
            "boolean": "BooleanField",
            "datetime": "DateTimeField",
            "date": "DateField",
            "time": "TimeField",
            "text": "TextField",
            "json": "JSONField",
            "binary": "BinaryField",
            "email": "EmailField",
            "url": "URLField",
            "uuid": "UUIDField",
            "decimal": "DecimalField",
            "file": "FileField",
            "image": "ImageField",
        }

    def get_file_extension(self) -> str:
        """
        Возвращает расширение файла для Django.

        Returns:
            Расширение файла '.py'
        """
        return ".py"

    def get_field_type(self, field: Dict[str, Any]) -> str:
        """
        Возвращает тип поля Django на основе типа схемы.
        
        Args:
            field: Данные поля
            
        Returns:
            Тип поля Django
        """
        field_type = field.get("type", "string")
        supported_types = self.get_supported_types()
        
        # Специальная обработка для некоторых типов
        if field_type == "string":
            if field.get("max_length"):
                return "CharField"
            else:
                return "TextField"
        elif field_type == "integer":
            if field.get("is_primary_key"):
                return "AutoField"
            else:
                return "IntegerField"
        elif field_type == "decimal":
            return "DecimalField"
        
        return supported_types.get(field_type, "CharField")

    def get_field_parameters(self, field: Dict[str, Any]) -> Dict[str, Any]:
        """
        Возвращает параметры поля Django.
        
        Args:
            field: Данные поля
            
        Returns:
            Словарь параметров поля
        """
        params = {}
        
        # Максимальная длина для CharField
        if field.get("max_length"):
            params["max_length"] = field["max_length"]
        
        # Значение по умолчанию
        if field.get("default_value") is not None:
            params["default"] = field["default_value"]
        
        # Уникальность
        if field.get("is_unique"):
            params["unique"] = True
        
        # Nullable
        if field.get("is_nullable") is False:
            params["null"] = False
        elif field.get("is_nullable") is True:
            params["null"] = True
        
        # Blank (для форм)
        if field.get("blank") is not None:
            params["blank"] = field["blank"]
        
        # Help text
        if field.get("help_text"):
            params["help_text"] = field["help_text"]
        
        # Verbose name
        if field.get("verbose_name"):
            params["verbose_name"] = field["verbose_name"]
        
        # Choices
        if field.get("choices"):
            params["choices"] = field["choices"]
        
        # Decimal field parameters
        if field.get("type") == "decimal":
            if field.get("max_digits"):
                params["max_digits"] = field["max_digits"]
            if field.get("decimal_places"):
                params["decimal_places"] = field["decimal_places"]
        
        return params
