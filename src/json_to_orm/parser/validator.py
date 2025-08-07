"""
Валидатор схем данных.

Этот модуль содержит классы для валидации JSON-схем данных,
используемых для генерации ORM моделей.
"""

from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

from ..utils.logger import get_logger

logger = get_logger(__name__)


@dataclass
class ValidationResult:
    """Результат валидации схемы."""

    is_valid: bool
    table_count: int
    relationship_count: int
    errors: List[str]


class SchemaValidator:
    """Валидатор JSON-схемы"""
    
    def __init__(self):
        self.supported_types = {
            # Базовые типы
            "string", "integer", "float", "boolean", "datetime", "date", "time", "text",
            # Расширенные типы
            "uuid", "json", "jsonb", "array", "enum", "decimal", "binary", "blob",
            # Географические типы
            "point", "line", "polygon", "geometry",
            # Специальные типы
            "email", "url", "ip", "mac", "phone", "currency"
        }
        
        self.type_mappings = {
            # UUID типы
            "uuid": ["uuid", "guid", "uniqueidentifier"],
            # JSON типы  
            "json": ["json", "jsonb", "json_type"],
            # Массивы
            "array": ["array", "list", "set"],
            # Перечисления
            "enum": ["enum", "choice", "select"],
            # Decimal типы
            "decimal": ["decimal", "numeric", "money"],
            # Binary типы
            "binary": ["binary", "blob", "bytea", "varbinary"],
            # Географические типы
            "point": ["point", "geography", "geometry"],
            # Специальные типы
            "email": ["email", "mail"],
            "url": ["url", "uri", "link"],
            "ip": ["ip", "inet", "ipaddress"],
            "mac": ["mac", "macaddress"],
            "phone": ["phone", "telephone"],
            "currency": ["currency", "money", "price"]
        }

    def validate_schema(self, schema_data: dict) -> ValidationResult:
        """Валидация схемы данных"""
        errors = []
        
        # Проверка структуры схемы
        if not isinstance(schema_data, dict):
            errors.append("Schema must be a JSON object")
            return ValidationResult(False, 0, 0, errors)
        
        # Проверка обязательных полей
        if "tables" not in schema_data:
            errors.append("Schema must contain 'tables' field")
        
        # Валидация таблиц
        if "tables" in schema_data:
            table_errors = self._validate_tables(schema_data["tables"])
            errors.extend(table_errors)
        
        # Валидация связей
        if "relationships" in schema_data:
            relationship_errors = self._validate_relationships(schema_data["relationships"])
            errors.extend(relationship_errors)
        
        # Валидация метаданных
        if "metadata" in schema_data:
            metadata_errors = self._validate_metadata(schema_data["metadata"])
            errors.extend(metadata_errors)
        
        table_count = len(schema_data.get("tables", []))
        relationship_count = len(schema_data.get("relationships", []))
        return ValidationResult(len(errors) == 0, table_count, relationship_count, errors)

    def _validate_tables(self, tables: list) -> list:
        """Валидация таблиц"""
        errors = []
        table_names = set()
        
        if not isinstance(tables, list):
            errors.append("Tables must be an array")
            return errors
        
        for i, table in enumerate(tables):
            if not isinstance(table, dict):
                errors.append(f"Table at index {i} must be an object")
                continue
            
            # Проверка имени таблицы
            if "name" not in table:
                errors.append(f"Table at index {i} must have a 'name' field")
                continue
            
            table_name = table["name"]
            if not isinstance(table_name, str):
                errors.append(f"Table name at index {i} must be a string")
                continue
            
            if table_name in table_names:
                errors.append(f"Duplicate table name: {table_name}")
            else:
                table_names.add(table_name)
            
            # Валидация полей таблицы
            if "fields" in table:
                field_errors = self._validate_fields(table["fields"], table_name)
                errors.extend(field_errors)
            
            # Валидация индексов
            if "indexes" in table:
                index_errors = self._validate_indexes(table["indexes"], table_name)
                errors.extend(index_errors)
        
        return errors

    def _validate_fields(self, fields: list, table_name: str) -> list:
        """Валидация полей таблицы"""
        errors = []
        field_names = set()
        
        if not isinstance(fields, list):
            errors.append(f"Fields in table '{table_name}' must be an array")
            return errors
        
        for i, field in enumerate(fields):
            if not isinstance(field, dict):
                errors.append(f"Field at index {i} in table '{table_name}' must be an object")
                continue
            
            # Проверка имени поля
            if "name" not in field:
                errors.append(f"Field at index {i} in table '{table_name}' must have a 'name' field")
                continue
            
            field_name = field["name"]
            if not isinstance(field_name, str):
                errors.append(f"Field name at index {i} in table '{table_name}' must be a string")
                continue
            
            if field_name in field_names:
                errors.append(f"Duplicate field name '{field_name}' in table '{table_name}'")
            else:
                field_names.add(field_name)
            
            # Валидация типа поля
            if "type" in field:
                type_errors = self._validate_field_type(field["type"], field_name, table_name)
                errors.extend(type_errors)
            
            # Валидация ограничений
            constraint_errors = self._validate_field_constraints(field, field_name, table_name)
            errors.extend(constraint_errors)
        
        return errors

    def _validate_field_type(self, field_type: str, field_name: str, table_name: str) -> list:
        """Валидация типа поля"""
        errors = []
        
        if not isinstance(field_type, str):
            errors.append(f"Field type for '{field_name}' in table '{table_name}' must be a string")
            return errors
        
        # Проверка базового типа
        if field_type not in self.supported_types:
            # Проверка алиасов типов
            found_in_aliases = False
            for base_type, aliases in self.type_mappings.items():
                if field_type in aliases:
                    found_in_aliases = True
                    break
            
            if not found_in_aliases:
                errors.append(f"Unsupported field type '{field_type}' for field '{field_name}' in table '{table_name}'. Supported types: {', '.join(sorted(self.supported_types))}")
        
        return errors

    def _validate_field_constraints(self, field: dict, field_name: str, table_name: str) -> list:
        """Валидация ограничений поля"""
        errors = []
        
        # Проверка boolean ограничений
        boolean_constraints = ["is_primary_key", "is_unique", "is_nullable", "is_auto_increment"]
        for constraint in boolean_constraints:
            if constraint in field and not isinstance(field[constraint], bool):
                errors.append(f"Constraint '{constraint}' for field '{field_name}' in table '{table_name}' must be a boolean")
        
        # Проверка default_value
        if "default_value" in field:
            if not isinstance(field["default_value"], (str, int, float, bool)) and field["default_value"] is not None:
                errors.append(f"Default value for field '{field_name}' in table '{table_name}' must be a primitive type")
        
        # Проверка max_length для строковых типов
        if "max_length" in field:
            if not isinstance(field["max_length"], int) or field["max_length"] <= 0:
                errors.append(f"Max length for field '{field_name}' in table '{table_name}' must be a positive integer")
        
        # Проверка precision и scale для decimal
        if "precision" in field:
            if not isinstance(field["precision"], int) or field["precision"] <= 0:
                errors.append(f"Precision for field '{field_name}' in table '{table_name}' must be a positive integer")
        
        if "scale" in field:
            if not isinstance(field["scale"], int) or field["scale"] < 0:
                errors.append(f"Scale for field '{field_name}' in table '{table_name}' must be a non-negative integer")
        
        # Проверка enum_values
        if "enum_values" in field:
            if not isinstance(field["enum_values"], list):
                errors.append(f"Enum values for field '{field_name}' in table '{table_name}' must be an array")
            else:
                for i, value in enumerate(field["enum_values"]):
                    if not isinstance(value, (str, int)):
                        errors.append(f"Enum value at index {i} for field '{field_name}' in table '{table_name}' must be a string or integer")
        
        return errors

    def _validate_indexes(self, indexes: list, table_name: str) -> list:
        """Валидация индексов"""
        errors = []
        
        if not isinstance(indexes, list):
            errors.append(f"Indexes in table '{table_name}' must be an array")
            return errors
        
        for i, index in enumerate(indexes):
            if not isinstance(index, dict):
                errors.append(f"Index at index {i} in table '{table_name}' must be an object")
                continue
            
            # Проверка обязательных полей индекса
            if "name" not in index:
                errors.append(f"Index at index {i} in table '{table_name}' must have a 'name' field")
            
            if "fields" not in index:
                errors.append(f"Index at index {i} in table '{table_name}' must have a 'fields' field")
            elif not isinstance(index["fields"], list):
                errors.append(f"Index fields at index {i} in table '{table_name}' must be an array")
            
            # Проверка типа индекса
            if "type" in index:
                valid_types = ["btree", "hash", "gin", "gist", "spgist", "brin"]
                if index["type"] not in valid_types:
                    errors.append(f"Invalid index type '{index['type']}' at index {i} in table '{table_name}'. Valid types: {', '.join(valid_types)}")
        
        return errors

    def _validate_relationships(self, relationships: list) -> list:
        """Валидация связей между таблицами"""
        errors = []
        
        if not isinstance(relationships, list):
            errors.append("Relationships must be an array")
            return errors
        
        for i, relationship in enumerate(relationships):
            if not isinstance(relationship, dict):
                errors.append(f"Relationship at index {i} must be an object")
                continue
            
            # Проверка обязательных полей (поддерживаем оба формата)
            if "from" in relationship and "to" in relationship:
                # Новый формат
                from_table = relationship["from"]
                to_table = relationship["to"]
            elif "table" in relationship and "related_table" in relationship:
                # Старый формат
                from_table = relationship["table"]
                to_table = relationship["related_table"]
            else:
                errors.append(f"Relationship at index {i} must have either 'from'/'to' or 'table'/'related_table' fields")
                continue
            
            if "type" not in relationship:
                errors.append(f"Relationship at index {i} must have a 'type' field")
            
            # Проверка типа связи
            if "type" in relationship:
                valid_types = ["one_to_one", "one_to_many", "many_to_one", "many_to_many"]
                if relationship["type"] not in valid_types:
                    errors.append(f"Invalid relationship type '{relationship['type']}' at index {i}. Valid types: {', '.join(valid_types)}")
            
            # Проверка каскадных операций
            if "on_delete" in relationship:
                valid_actions = ["cascade", "set_null", "restrict", "no_action"]
                if relationship["on_delete"] not in valid_actions:
                    errors.append(f"Invalid on_delete action '{relationship['on_delete']}' at index {i}. Valid actions: {', '.join(valid_actions)}")
            
            if "on_update" in relationship:
                valid_actions = ["cascade", "set_null", "restrict", "no_action"]
                if relationship["on_update"] not in valid_actions:
                    errors.append(f"Invalid on_update action '{relationship['on_update']}' at index {i}. Valid actions: {', '.join(valid_actions)}")
        
        return errors

    def _validate_metadata(self, metadata: dict) -> list:
        """Валидация метаданных схемы"""
        errors = []
        
        if not isinstance(metadata, dict):
            errors.append("Metadata must be an object")
            return errors
        
        # Проверка версии схемы
        if "version" in metadata:
            if not isinstance(metadata["version"], str):
                errors.append("Schema version must be a string")
        
        # Проверка автора
        if "author" in metadata:
            if not isinstance(metadata["author"], str):
                errors.append("Schema author must be a string")
        
        # Проверка описания
        if "description" in metadata:
            if not isinstance(metadata["description"], str):
                errors.append("Schema description must be a string")
        
        # Проверка тегов
        if "tags" in metadata:
            if not isinstance(metadata["tags"], list):
                errors.append("Schema tags must be an array")
            else:
                for i, tag in enumerate(metadata["tags"]):
                    if not isinstance(tag, str):
                        errors.append(f"Tag at index {i} must be a string")
        
        return errors
