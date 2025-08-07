"""
Тесты для модуля парсинга JSON-схем.
"""

import pytest
import json
from pathlib import Path
from unittest.mock import mock_open, patch

from json_to_orm.parser.json_parser import JSONParser
from json_to_orm.parser.validator import SchemaValidator
# Импорты исключений больше не нужны, так как мы используем стандартные


class TestJSONParser:
    """Тесты для JSON парсера."""

    def test_parse_valid_json_file(self):
        """Тест парсинга валидного JSON файла."""
        valid_schema = {
            "tables": [
                {
                    "name": "users",
                    "fields": [
                        {
                            "name": "id",
                            "type": "integer",
                            "primary_key": True,
                            "auto_increment": True
                        },
                        {
                            "name": "email",
                            "type": "string",
                            "unique": True,
                            "nullable": False
                        }
                    ]
                }
            ],
            "relationships": []
        }
        
        with patch("builtins.open", mock_open(read_data=json.dumps(valid_schema))), \
             patch("pathlib.Path.exists", return_value=True), \
             patch("pathlib.Path.is_file", return_value=True):
            parser = JSONParser()
            result = parser.parse_file("schema.json")
            
            assert result["tables"] == valid_schema["tables"]
            assert result["relationships"] == valid_schema["relationships"]

    def test_parse_invalid_json_file(self):
        """Тест парсинга невалидного JSON файла."""
        invalid_json = "{ invalid json content }"
        
        with patch("builtins.open", mock_open(read_data=invalid_json)), \
             patch("pathlib.Path.exists", return_value=True), \
             patch("pathlib.Path.is_file", return_value=True):
            parser = JSONParser()
            with pytest.raises(json.JSONDecodeError):
                parser.parse_file("schema.json")

    def test_parse_missing_file(self):
        """Тест парсинга несуществующего файла."""
        parser = JSONParser()
        with pytest.raises(FileNotFoundError):
            parser.parse_file("nonexistent.json")

    def test_parse_empty_file(self):
        """Тест парсинга пустого файла."""
        with patch("builtins.open", mock_open(read_data="")), \
             patch("pathlib.Path.exists", return_value=True), \
             patch("pathlib.Path.is_file", return_value=True):
            parser = JSONParser()
            with pytest.raises(json.JSONDecodeError):
                parser.parse_file("empty.json")

    def test_parse_with_encoding(self):
        """Тест парсинга файла с указанной кодировкой."""
        valid_schema = {"tables": [], "relationships": []}

        with patch("builtins.open", mock_open(read_data=json.dumps(valid_schema))), \
             patch("pathlib.Path.exists", return_value=True), \
             patch("pathlib.Path.is_file", return_value=True):
            parser = JSONParser()
            result = parser.parse_file("schema.json")
            
            assert result["tables"] == []
            assert result["relationships"] == []


class TestSchemaValidator:
    """Тесты для валидатора схемы."""

    def test_validate_valid_schema(self):
        """Тест валидации корректной схемы."""
        valid_schema = {
            "tables": [
                {
                    "name": "users",
                    "fields": [
                        {
                            "name": "id",
                            "type": "integer",
                            "primary_key": True
                        },
                        {
                            "name": "email",
                            "type": "string",
                            "unique": True
                        }
                    ]
                }
            ],
            "relationships": []
        }
        
        validator = SchemaValidator()
        result = validator.validate_schema(valid_schema)
        
        assert result.is_valid is True

    def test_validate_missing_tables(self):
        """Тест валидации схемы без таблиц."""
        invalid_schema = {"relationships": []}
        
        validator = SchemaValidator()
        result = validator.validate_schema(invalid_schema)
        assert not result.is_valid
        assert len(result.errors) > 0

    def test_validate_empty_tables(self):
        """Тест валидации схемы с пустыми таблицами."""
        schema = {"tables": [], "relationships": []}
        
        validator = SchemaValidator()
        result = validator.validate_schema(schema)
        # Пустые таблицы должны быть валидными
        assert result.is_valid

    def test_validate_table_without_fields(self):
        """Тест валидации таблицы без полей."""
        schema = {
            "tables": [
                {
                    "name": "users",
                    "fields": []
                }
            ],
            "relationships": []
        }
        
        validator = SchemaValidator()
        result = validator.validate_schema(schema)
        # Таблица без полей должна быть валидной
        assert result.is_valid

    def test_validate_invalid_field_type(self):
        """Тест валидации поля с невалидным типом."""
        schema = {
            "tables": [
                {
                    "name": "users",
                    "fields": [
                        {
                            "name": "id",
                            "type": "invalid_type"
                        }
                    ]
                }
            ],
            "relationships": []
        }
        
        validator = SchemaValidator()
        result = validator.validate_schema(schema)
        assert not result.is_valid
        assert len(result.errors) > 0
        assert any("invalid_type" in error for error in result.errors)

    def test_validate_duplicate_table_names(self):
        """Тест валидации схемы с дублирующимися именами таблиц."""
        schema = {
            "tables": [
                {
                    "name": "users",
                    "fields": [{"name": "id", "type": "integer"}]
                },
                {
                    "name": "users",
                    "fields": [{"name": "id", "type": "integer"}]
                }
            ],
            "relationships": []
        }
        
        validator = SchemaValidator()
        result = validator.validate_schema(schema)
        assert not result.is_valid
        assert len(result.errors) > 0
        assert any("Duplicate table name" in error for error in result.errors)

    def test_validate_duplicate_field_names(self):
        """Тест валидации таблицы с дублирующимися именами полей."""
        schema = {
            "tables": [
                {
                    "name": "users",
                    "fields": [
                        {"name": "id", "type": "integer"},
                        {"name": "id", "type": "string"}
                    ]
                }
            ],
            "relationships": []
        }
        
        validator = SchemaValidator()
        result = validator.validate_schema(schema)
        assert not result.is_valid
        assert len(result.errors) > 0
        assert any("Duplicate field name" in error for error in result.errors)

    def test_validate_invalid_relationship(self):
        """Тест валидации невалидной связи."""
        schema = {
            "tables": [
                {
                    "name": "users",
                    "fields": [{"name": "id", "type": "integer"}]
                }
            ],
            "relationships": [
                {
                    "from": "users",
                    "to": "posts",
                    "type": "invalid_type"  # Невалидный тип связи
                }
            ]
        }
        
        validator = SchemaValidator()
        result = validator.validate_schema(schema)
        assert not result.is_valid
        assert len(result.errors) > 0

    def test_validate_complex_schema(self):
        """Тест валидации сложной схемы с множественными таблицами и связями."""
        schema = {
            "tables": [
                {
                    "name": "users",
                    "fields": [
                        {"name": "id", "type": "integer", "primary_key": True},
                        {"name": "email", "type": "string", "unique": True},
                        {"name": "name", "type": "string"},
                        {"name": "created_at", "type": "datetime"}
                    ]
                },
                {
                    "name": "posts",
                    "fields": [
                        {"name": "id", "type": "integer", "primary_key": True},
                        {"name": "title", "type": "string"},
                        {"name": "content", "type": "text"},
                        {"name": "user_id", "type": "integer"},
                        {"name": "created_at", "type": "datetime"}
                    ]
                }
            ],
            "relationships": [
                {
                    "from": "users",
                    "to": "posts",
                    "type": "one_to_many",
                    "foreign_key": "user_id"
                }
            ]
        }
        
        validator = SchemaValidator()
        result = validator.validate_schema(schema)
        
        assert result.is_valid is True

    def test_validate_field_constraints(self):
        """Тест валидации ограничений полей."""
        schema = {
            "tables": [
                {
                    "name": "users",
                    "fields": [
                        {
                            "name": "id",
                            "type": "integer",
                            "primary_key": True,
                            "auto_increment": True
                        },
                        {
                            "name": "email",
                            "type": "string",
                            "unique": True,
                            "nullable": False,
                            "max_length": 255
                        },
                        {
                            "name": "age",
                            "type": "integer",
                            "min_value": 0,
                            "max_value": 150
                        }
                    ]
                }
            ],
            "relationships": []
        }
        
        validator = SchemaValidator()
        result = validator.validate_schema(schema)
        
        assert result.is_valid is True

    def test_validate_unsupported_constraint(self):
        """Тест валидации неподдерживаемого ограничения."""
        schema = {
            "tables": [
                {
                    "name": "users",
                    "fields": [
                        {
                            "name": "id",
                            "type": "integer",
                            "unsupported_constraint": True
                        }
                    ]
                }
            ],
            "relationships": []
        }
        
        validator = SchemaValidator()
        # Должно пройти валидацию, игнорируя неподдерживаемые ограничения
        result = validator.validate_schema(schema)
        
        assert result.is_valid is True


class TestParserIntegration:
    """Интеграционные тесты для парсера и валидатора."""

    def test_parse_and_validate_valid_schema(self):
        """Тест полного цикла парсинга и валидации валидной схемы."""
        valid_schema = {
            "tables": [
                {
                    "name": "users",
                    "fields": [
                        {"name": "id", "type": "integer", "primary_key": True},
                        {"name": "email", "type": "string", "unique": True}
                    ]
                }
            ],
            "relationships": []
        }
        
        with patch("builtins.open", mock_open(read_data=json.dumps(valid_schema))), \
             patch("pathlib.Path.exists", return_value=True), \
             patch("pathlib.Path.is_file", return_value=True):
            parser = JSONParser()
            validator = SchemaValidator()
            
            parsed_schema = parser.parse_file("schema.json")
            result = validator.validate_schema(parsed_schema)
            
            assert result.is_valid is True
            assert parsed_schema["tables"][0]["name"] == "users"

    def test_parse_and_validate_invalid_schema(self):
        """Тест полного цикла парсинга и валидации невалидной схемы."""
        invalid_schema = {
            "tables": [
                {
                    "name": "users",
                    "fields": [
                        {"name": "id", "type": "invalid_type"}
                    ]
                }
            ],
            "relationships": []
        }
        
        with patch("builtins.open", mock_open(read_data=json.dumps(invalid_schema))), \
             patch("pathlib.Path.exists", return_value=True), \
             patch("pathlib.Path.is_file", return_value=True):
            parser = JSONParser()
            validator = SchemaValidator()
            
            parsed_schema = parser.parse_file("schema.json")
            result = validator.validate_schema(parsed_schema)
            assert not result.is_valid
            assert len(result.errors) > 0 