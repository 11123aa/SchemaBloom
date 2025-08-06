"""
JSON-to-ORM: CLI-утилита для генерации ORM моделей из JSON-схем.

Этот пакет предоставляет функциональность для автоматической генерации
моделей для популярных ORM фреймворков (Prisma, Django, SQLAlchemy)
на основе JSON-схем данных.
"""

__version__ = "0.1.0"
__author__ = "JSON-to-ORM Team"
__email__ = "team@json-to-orm.com"

from .cli import main
from .core import JSONToORM

__all__ = ["main", "JSONToORM"]
