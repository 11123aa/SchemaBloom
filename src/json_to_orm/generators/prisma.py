"""
Генератор Prisma моделей.

Этот модуль содержит генератор для создания Prisma схем
на основе JSON-схем данных.
"""

from pathlib import Path
from typing import Any, Dict, List

from .base import BaseGenerator


class PrismaGenerator(BaseGenerator):
    """
    Генератор Prisma моделей.

    Этот класс генерирует Prisma схемы на основе JSON-схем данных.
    """

    def __init__(self) -> None:
        """Инициализация Prisma генератора."""
        super().__init__()

    def generate_models(
        self, schema_data: Dict[str, Any], output_dir: str
    ) -> List[str]:
        """
        Генерирует Prisma модели на основе схемы данных.

        Args:
            schema_data: Данные схемы
            output_dir: Директория для сохранения файлов

        Returns:
            Список путей к созданным файлов
        """
        if not self.validate_schema(schema_data):
            self.logger.error("Схема данных невалидна для Prisma генератора")
            return []

        # Создаем выходную директорию
        output_path = self.create_output_directory(output_dir)
        
        # Подготавливаем данные для шаблона
        tables = schema_data.get("tables", [])
        processed_tables = []
        
        for table in tables:
            processed_table = self._process_table(table, schema_data.get("relationships", []))
            processed_tables.append(processed_table)
        
        # Рендерим шаблон схемы
        template = self.template_engine.get_template("prisma/schema.j2")
        content = template.render(tables=processed_tables)
        
        # Сохраняем файл
        file_path = output_path / f"schema{self.get_file_extension()}"
        self.write_file(file_path, content)
        
        self.logger.info(f"Создан файл Prisma схемы: {file_path}")
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
        Возвращает словарь поддерживаемых типов данных Prisma.

        Returns:
            Словарь {тип_схемы: тип_prisma}
        """
        return {
            "string": "String",
            "integer": "Int",
            "float": "Float",
            "boolean": "Boolean",
            "datetime": "DateTime",
            "date": "DateTime",
            "time": "DateTime",
            "text": "String",
            "json": "Json",
            "binary": "Bytes",
        }

    def get_file_extension(self) -> str:
        """
        Возвращает расширение файла для Prisma.

        Returns:
            Расширение файла '.prisma'
        """
        return ".prisma"
