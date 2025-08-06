"""
Фильтры для Jinja2 шаблонов.

Этот модуль содержит фильтры для форматирования имен и типов данных
в различных ORM фреймворках.
"""

import re
from typing import Any


def pascal_case(value: str) -> str:
    """
    Преобразует строку в PascalCase.
    
    Args:
        value: Исходная строка
        
    Returns:
        Строка в PascalCase
    """
    if not value:
        return value
    
    # Разбиваем по подчеркиваниям и дефисам
    words = re.split(r'[_-]', value)
    # Капитализируем каждое слово
    return ''.join(word.capitalize() for word in words)


def snake_case(value: str) -> str:
    """
    Преобразует строку в snake_case.
    
    Args:
        value: Исходная строка
        
    Returns:
        Строка в snake_case
    """
    if not value:
        return value
    
    # Заменяем пробелы и дефисы на подчеркивания
    value = re.sub(r'[\s-]', '_', value)
    # Приводим к нижнему регистру
    return value.lower()


def camel_case(value: str) -> str:
    """
    Преобразует строку в camelCase.
    
    Args:
        value: Исходная строка
        
    Returns:
        Строка в camelCase
    """
    if not value:
        return value
    
    # Сначала преобразуем в PascalCase
    pascal = pascal_case(value)
    # Затем делаем первую букву строчной
    return pascal[0].lower() + pascal[1:]


def prisma_type(value: str) -> str:
    """
    Преобразует тип данных в Prisma тип.
    
    Args:
        value: Исходный тип данных
        
    Returns:
        Prisma тип данных
    """
    type_mapping = {
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
        "decimal": "Decimal",
        "uuid": "String",
        "email": "String",
        "url": "String",
        "phone": "String",
    }
    
    return type_mapping.get(value.lower(), "String")


def django_type(value: str) -> str:
    """
    Преобразует тип данных в Django тип.
    
    Args:
        value: Исходный тип данных
        
    Returns:
        Django тип данных
    """
    type_mapping = {
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
        "decimal": "DecimalField",
        "uuid": "UUIDField",
        "email": "EmailField",
        "url": "URLField",
    }
    
    return type_mapping.get(value.lower(), "CharField")


def sqlalchemy_type(value: str) -> str:
    """
    Преобразует тип данных в SQLAlchemy тип.
    
    Args:
        value: Исходный тип данных
        
    Returns:
        SQLAlchemy тип данных
    """
    type_mapping = {
        "string": "String",
        "integer": "Integer",
        "float": "Float",
        "boolean": "Boolean",
        "datetime": "DateTime",
        "date": "Date",
        "time": "Time",
        "text": "Text",
        "json": "JSON",
        "binary": "LargeBinary",
        "decimal": "Numeric",
        "uuid": "String",
        "email": "String",
        "url": "String",
    }
    
    return type_mapping.get(value.lower(), "String")


def format_default_value(value: Any, field_type: str) -> str:
    """
    Форматирует значение по умолчанию для поля.
    
    Args:
        value: Значение по умолчанию
        field_type: Тип поля
        
    Returns:
        Отформатированное значение
    """
    if value is None:
        return ""
    
    if field_type.lower() in ["string", "text", "email", "url", "uuid"]:
        return f'"{value}"'
    elif field_type.lower() in ["boolean"]:
        return str(value).lower()
    elif field_type.lower() in ["datetime", "date", "time"]:
        return f'"{value}"'
    else:
        return str(value)


def get_imports_for_type(field_type: str, framework: str) -> str:
    """
    Возвращает необходимые импорты для типа данных.
    
    Args:
        field_type: Тип поля
        framework: Фреймворк (prisma, django, sqlalchemy)
        
    Returns:
        Строка с импортами
    """
    if framework.lower() == "django":
        if field_type.lower() in ["uuid"]:
            return "import uuid"
        elif field_type.lower() in ["decimal"]:
            return "from decimal import Decimal"
        elif field_type.lower() in ["datetime", "date", "time"]:
            return "from django.utils import timezone"
    elif framework.lower() == "sqlalchemy":
        if field_type.lower() in ["uuid"]:
            return "import uuid"
        elif field_type.lower() in ["decimal"]:
            return "from decimal import Decimal"
        elif field_type.lower() in ["datetime", "date", "time"]:
            return "from datetime import datetime, date, time"
    
    return ""


# Регистрируем все фильтры
FILTERS = {
    "pascal_case": pascal_case,
    "snake_case": snake_case,
    "camel_case": camel_case,
    "prisma_type": prisma_type,
    "django_type": django_type,
    "sqlalchemy_type": sqlalchemy_type,
    "format_default_value": format_default_value,
    "get_imports_for_type": get_imports_for_type,
} 