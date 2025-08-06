"""
Генератор Prisma моделей.

Этот модуль содержит генератор для создания Prisma схем
на основе JSON-схем данных.
"""

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
            Список путей к созданным файлам
        """
        # TODO: Реализовать генерацию Prisma моделей
        self.logger.info("Генерация Prisma моделей пока не реализована")
        return []

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
