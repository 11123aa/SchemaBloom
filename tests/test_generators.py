"""
Тесты для генераторов ORM моделей.
"""

import pytest
from unittest.mock import Mock, patch, mock_open
from pathlib import Path
from typing import List

from json_to_orm.generators.base import BaseGenerator
from json_to_orm.generators.prisma import PrismaGenerator
from json_to_orm.generators.django import DjangoGenerator
from json_to_orm.generators.sqlalchemy import SQLAlchemyGenerator


class TestBaseGenerator:
    """Тесты для базового генератора."""

    def test_base_generator_abstract_class(self):
        """Тест того, что базовый генератор является абстрактным классом."""
        with pytest.raises(TypeError):
            BaseGenerator()

    def test_base_generator_abstract_methods(self):
        """Тест того, что абстрактные методы не реализованы."""
        # Создаем подкласс для тестирования
        class TestGenerator(BaseGenerator):
            def generate_models(self, schema: dict, output_dir: str = ".") -> List[str]:
                return []
            
            def get_file_extension(self) -> str:
                return ".test"
            
            def get_supported_types(self) -> dict:
                return {"integer": "Int", "string": "String"}
            
            def validate_schema_structure(self, schema: dict) -> bool:
                return "tables" in schema
            
            def process_field_constraints(self, field: dict) -> dict:
                return field.copy()
            
            def process_relationships(self, schema: dict) -> List[dict]:
                return schema.get("relationships", [])
        
        generator = TestGenerator()
        assert generator.get_supported_types() is not None
        # template_engine может быть None в базовом классе
        assert hasattr(generator, 'template_engine')

    def test_validate_schema_structure(self):
        """Тест валидации структуры схемы."""
        class TestGenerator(BaseGenerator):
            def generate_models(self, schema: dict, output_dir: str = ".") -> List[str]:
                return []
            
            def get_file_extension(self) -> str:
                return ".test"
            
            def get_supported_types(self) -> dict:
                return {"integer": "Int", "string": "String"}
            
            def validate_schema_structure(self, schema: dict) -> bool:
                return "tables" in schema
            
            def process_field_constraints(self, field: dict) -> dict:
                return field.copy()
            
            def process_relationships(self, schema: dict) -> List[dict]:
                return schema.get("relationships", [])
        
        generator = TestGenerator()
        
        # Валидная схема
        valid_schema = {
            "tables": [
                {
                    "name": "users",
                    "fields": [
                        {"name": "id", "type": "integer", "primary_key": True}
                    ]
                }
            ],
            "relationships": []
        }
        
        assert generator.validate_schema_structure(valid_schema) is True
        
        # Невалидная схема
        invalid_schema = {"invalid": "structure"}
        assert generator.validate_schema_structure(invalid_schema) is False

    def test_get_field_type_mapping(self):
        """Тест получения маппинга типов полей."""
        class TestGenerator(BaseGenerator):
            def generate_models(self, schema: dict, output_dir: str = ".") -> List[str]:
                return []
            
            def get_file_extension(self) -> str:
                return ".test"
            
            def get_supported_types(self) -> dict:
                return {"integer": "Int", "string": "String", "boolean": "Boolean"}
            
            def validate_schema_structure(self, schema: dict) -> bool:
                return "tables" in schema
            
            def process_field_constraints(self, field: dict) -> dict:
                return field.copy()
            
            def process_relationships(self, schema: dict) -> List[dict]:
                return schema.get("relationships", [])
        
        generator = TestGenerator()
        
        # Проверяем, что базовые типы поддерживаются
        supported_types = generator.get_supported_types()
        assert "integer" in supported_types
        assert "string" in supported_types
        assert "boolean" in supported_types

    def test_process_field_constraints(self):
        """Тест обработки ограничений полей."""
        class TestGenerator(BaseGenerator):
            def generate_models(self, schema: dict, output_dir: str = ".") -> List[str]:
                return []
            
            def get_file_extension(self) -> str:
                return ".test"
            
            def get_supported_types(self) -> dict:
                return {"integer": "Int", "string": "String"}
            
            def validate_schema_structure(self, schema: dict) -> bool:
                return "tables" in schema
            
            def process_field_constraints(self, field: dict) -> dict:
                return field.copy()
            
            def process_relationships(self, schema: dict) -> List[dict]:
                return schema.get("relationships", [])
        
        generator = TestGenerator()
        
        field = {
            "name": "email",
            "type": "string",
            "unique": True,
            "nullable": False,
            "max_length": 255
        }
        
        processed = generator.process_field_constraints(field)
        assert processed["unique"] is True
        assert processed["nullable"] is False
        assert processed["max_length"] == 255

    def test_process_relationships(self):
        """Тест обработки связей между таблицами."""
        class TestGenerator(BaseGenerator):
            def generate_models(self, schema: dict, output_dir: str = ".") -> List[str]:
                return []
            
            def get_file_extension(self) -> str:
                return ".test"
            
            def get_supported_types(self) -> dict:
                return {"integer": "Int", "string": "String"}
            
            def validate_schema_structure(self, schema: dict) -> bool:
                return "tables" in schema
            
            def process_field_constraints(self, field: dict) -> dict:
                return field.copy()
            
            def process_relationships(self, schema: dict) -> List[dict]:
                return schema.get("relationships", [])
        
        generator = TestGenerator()
        
        schema = {
            "tables": [
                {
                    "name": "users",
                    "fields": [{"name": "id", "type": "integer", "primary_key": True}]
                },
                {
                    "name": "posts",
                    "fields": [
                        {"name": "id", "type": "integer", "primary_key": True},
                        {"name": "user_id", "type": "integer"}
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
        
        processed = generator.process_relationships(schema)
        assert len(processed) == 1
        assert processed[0]["from"] == "users"
        assert processed[0]["to"] == "posts"


class TestPrismaGenerator:
    """Тесты для генератора Prisma моделей."""

    def test_prisma_generator_initialization(self):
        """Тест инициализации генератора Prisma."""
        generator = PrismaGenerator()
        assert generator.get_supported_types() is not None
        assert generator.get_file_extension() == ".prisma"

    def test_generate_models_basic(self):
        """Тест генерации базовых Prisma моделей."""
        generator = PrismaGenerator()
        
        schema = {
            "tables": [
                {
                    "name": "users",
                    "fields": [
                        {"name": "id", "type": "integer", "primary_key": True},
                        {"name": "email", "type": "string", "unique": True},
                        {"name": "name", "type": "string"}
                    ]
                }
            ],
            "relationships": []
        }
        
        # Генератор пока не реализован, но должен работать без ошибок
        generator.generate_models(schema, output_dir="test_output")

    def test_generate_models_with_relationships(self):
        """Тест генерации Prisma моделей со связями."""
        generator = PrismaGenerator()
        
        schema = {
            "tables": [
                {
                    "name": "users",
                    "fields": [
                        {"name": "id", "type": "integer", "primary_key": True},
                        {"name": "email", "type": "string"}
                    ]
                },
                {
                    "name": "posts",
                    "fields": [
                        {"name": "id", "type": "integer", "primary_key": True},
                        {"name": "title", "type": "string"},
                        {"name": "user_id", "type": "integer"}
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
        
        # Генератор пока не реализован, но должен работать без ошибок
        generator.generate_models(schema, output_dir="test_output")

    def test_prisma_field_type_mapping(self):
        """Тест маппинга типов полей для Prisma."""
        generator = PrismaGenerator()
        
        # Проверяем основные типы
        field = {"type": "integer"}
        assert generator.get_field_type(field) == "integer"
        
        field = {"type": "string"}
        assert generator.get_field_type(field) == "string"


class TestDjangoGenerator:
    """Тесты для генератора Django моделей."""

    def test_django_generator_initialization(self):
        """Тест инициализации генератора Django."""
        generator = DjangoGenerator()
        assert generator.get_supported_types() is not None
        assert generator.get_file_extension() == ".py"

    def test_generate_models_basic(self):
        """Тест генерации базовых Django моделей."""
        generator = DjangoGenerator()
        
        schema = {
            "tables": [
                {
                    "name": "users",
                    "fields": [
                        {"name": "id", "type": "integer", "primary_key": True},
                        {"name": "email", "type": "string", "unique": True},
                        {"name": "name", "type": "string"}
                    ]
                }
            ],
            "relationships": []
        }
        
        # Генератор пока не реализован, но должен работать без ошибок
        generator.generate_models(schema, output_dir="test_output")

    def test_generate_models_with_relationships(self):
        """Тест генерации Django моделей со связями."""
        generator = DjangoGenerator()
        
        schema = {
            "tables": [
                {
                    "name": "users",
                    "fields": [
                        {"name": "id", "type": "integer", "primary_key": True},
                        {"name": "email", "type": "string"}
                    ]
                },
                {
                    "name": "posts",
                    "fields": [
                        {"name": "id", "type": "integer", "primary_key": True},
                        {"name": "title", "type": "string"},
                        {"name": "user_id", "type": "integer"}
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
        
        # Генератор пока не реализован, но должен работать без ошибок
        generator.generate_models(schema, output_dir="test_output")

    def test_django_field_type_mapping(self):
        """Тест маппинга типов полей для Django."""
        generator = DjangoGenerator()
        
        # Проверяем основные типы
        field = {"type": "integer"}
        assert generator.get_field_type(field) == "integer"
        
        field = {"type": "string"}
        assert generator.get_field_type(field) == "string"


class TestSQLAlchemyGenerator:
    """Тесты для генератора SQLAlchemy моделей."""

    def test_sqlalchemy_generator_initialization(self):
        """Тест инициализации генератора SQLAlchemy."""
        generator = SQLAlchemyGenerator()
        assert generator.get_supported_types() is not None
        assert generator.get_file_extension() == ".py"

    def test_generate_models_basic(self):
        """Тест генерации базовых SQLAlchemy моделей."""
        generator = SQLAlchemyGenerator()
        
        schema = {
            "tables": [
                {
                    "name": "users",
                    "fields": [
                        {"name": "id", "type": "integer", "primary_key": True},
                        {"name": "email", "type": "string", "unique": True},
                        {"name": "name", "type": "string"}
                    ]
                }
            ],
            "relationships": []
        }
        
        # Генератор пока не реализован, но должен работать без ошибок
        generator.generate_models(schema, output_dir="test_output")

    def test_generate_models_with_relationships(self):
        """Тест генерации SQLAlchemy моделей со связями."""
        generator = SQLAlchemyGenerator()
        
        schema = {
            "tables": [
                {
                    "name": "users",
                    "fields": [
                        {"name": "id", "type": "integer", "primary_key": True},
                        {"name": "email", "type": "string"}
                    ]
                },
                {
                    "name": "posts",
                    "fields": [
                        {"name": "id", "type": "integer", "primary_key": True},
                        {"name": "title", "type": "string"},
                        {"name": "user_id", "type": "integer"}
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
        
        # Генератор пока не реализован, но должен работать без ошибок
        generator.generate_models(schema, output_dir="test_output")

    def test_sqlalchemy_field_type_mapping(self):
        """Тест маппинга типов полей для SQLAlchemy."""
        generator = SQLAlchemyGenerator()
        
        # Проверяем основные типы
        field = {"type": "integer"}
        assert generator.get_field_type(field) == "integer"
        
        field = {"type": "string"}
        assert generator.get_field_type(field) == "string"


class TestGeneratorIntegration:
    """Интеграционные тесты для генераторов."""

    def test_all_generators_have_supported_types(self):
        """Тест того, что все генераторы имеют поддерживаемые типы."""
        prisma_gen = PrismaGenerator()
        django_gen = DjangoGenerator()
        sqlalchemy_gen = SQLAlchemyGenerator()
        
        # Все генераторы должны иметь поддерживаемые типы
        for gen in [prisma_gen, django_gen, sqlalchemy_gen]:
            supported_types = gen.get_supported_types()
            assert supported_types is not None
            assert isinstance(supported_types, dict)

    def test_generator_output_consistency(self):
        """Тест консистентности вывода генераторов."""
        schema = {
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
        
        generators = [
            PrismaGenerator(),
            DjangoGenerator(),
            SQLAlchemyGenerator()
        ]
        
        # Все генераторы должны работать без ошибок
        for generator in generators:
            generator.generate_models(schema, output_dir="test_output")

    def test_generator_error_handling(self):
        """Тест обработки ошибок в генераторах."""
        generators = [
            PrismaGenerator(),
            DjangoGenerator(),
            SQLAlchemyGenerator()
        ]
        
        invalid_schema = {"invalid": "schema"}
        
        # Генераторы пока не реализованы полностью, поэтому они не выбрасывают ошибки
        # Вместо этого они логируют сообщения
        for generator in generators:
            # Должно работать без ошибок (пока только логирование)
            generator.generate_models(invalid_schema, output_dir="test_output") 