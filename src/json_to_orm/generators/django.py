"""
Генератор Django моделей.

Этот модуль содержит генератор для создания Django моделей
на основе JSON-схем данных.
"""

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
            Список путей к созданным файлам
        """
        # TODO: Реализовать генерацию Django моделей
        self.logger.info("Генерация Django моделей пока не реализована")
        return []

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
        }

    def get_file_extension(self) -> str:
        """
        Возвращает расширение файла для Django.

        Returns:
            Расширение файла '.py'
        """
        return ".py"
