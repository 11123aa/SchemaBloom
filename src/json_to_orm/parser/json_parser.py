"""
JSON парсер для схем данных.

Этот модуль содержит классы для парсинга JSON-файлов,
содержащих схемы данных для генерации ORM моделей.
"""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from ..utils.logger import get_logger

logger = get_logger(__name__)


class JSONParser:
    """
    Парсер JSON-файлов со схемами данных.

    Этот класс отвечает за загрузку и парсинг JSON-файлов,
    содержащих схемы данных для генерации ORM моделей.
    """

    def __init__(self) -> None:
        """Инициализация парсера."""
        self.logger = logger

    def parse_file(self, file_path: Union[str, Path]) -> Dict[str, Any]:
        """
        Парсит JSON-файл и возвращает его содержимое.

        Args:
            file_path: Путь к JSON-файлу

        Returns:
            Словарь с данными из JSON-файла

        Raises:
            FileNotFoundError: Если файл не найден
            json.JSONDecodeError: Если файл содержит некорректный JSON
        """
        file_path = Path(file_path)

        if not file_path.exists():
            raise FileNotFoundError(f"Файл не найден: {file_path}")

        if not file_path.is_file():
            raise ValueError(f"Путь не является файлом: {file_path}")

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            self.logger.info(f"Успешно загружен файл: {file_path}")
            return data

        except json.JSONDecodeError as e:
            self.logger.error(f"Ошибка парсинга JSON в файле {file_path}: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Неожиданная ошибка при загрузке файла {file_path}: {e}")
            raise

    def parse_string(self, json_string: str) -> Dict[str, Any]:
        """
        Парсит JSON-строку и возвращает её содержимое.

        Args:
            json_string: JSON-строка для парсинга

        Returns:
            Словарь с данными из JSON-строки

        Raises:
            json.JSONDecodeError: Если строка содержит некорректный JSON
        """
        try:
            data = json.loads(json_string)
            self.logger.info("Успешно загружена JSON-строка")
            return data

        except json.JSONDecodeError as e:
            self.logger.error(f"Ошибка парсинга JSON-строки: {e}")
            raise

    def validate_schema_structure(self, data: Dict[str, Any]) -> bool:
        """
        Проверяет базовую структуру схемы данных.

        Args:
            data: Данные для проверки

        Returns:
            True если структура корректна, False иначе
        """
        if not isinstance(data, dict):
            self.logger.error("Схема должна быть объектом (словарем)")
            return False

        # Проверяем наличие обязательных полей
        required_fields = ["tables"]
        for field in required_fields:
            if field not in data:
                self.logger.error(f"Отсутствует обязательное поле: {field}")
                return False

        # Проверяем, что tables является списком
        if not isinstance(data["tables"], list):
            self.logger.error("Поле 'tables' должно быть массивом")
            return False

        self.logger.info("Базовая структура схемы корректна")
        return True

    def get_tables(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Извлекает список таблиц из схемы данных.

        Args:
            data: Данные схемы

        Returns:
            Список таблиц
        """
        return data.get("tables", [])

    def get_relationships(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Извлекает список связей из схемы данных.

        Args:
            data: Данные схемы

        Returns:
            Список связей
        """
        return data.get("relationships", [])
