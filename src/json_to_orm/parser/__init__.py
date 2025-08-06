"""
Модуль парсинга JSON-схем.

Этот модуль содержит классы для парсинга и валидации JSON-файлов,
содержащих схемы данных для генерации ORM моделей.
"""

from .json_parser import JSONParser
from .validator import SchemaValidator

__all__ = ["JSONParser", "SchemaValidator"] 