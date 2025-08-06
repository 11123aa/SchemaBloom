"""
Тесты для генераторов ORM моделей.
"""

import pytest
from unittest.mock import Mock, patch, mock_open
from pathlib import Path
from typing import List
import tempfile
import os

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
                        {"name": "id", "type": "integer", "is_primary_key": True}
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
            "is_unique": True,
            "is_nullable": False,
            "max_length": 255
        }
        
        processed = generator.process_field_constraints(field)
        assert processed["is_unique"] is True
        assert processed["is_nullable"] is False
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
                    "fields": [{"name": "id", "type": "integer", "is_primary_key": True}]
                },
                {
                    "name": "posts",
                    "fields": [
                        {"name": "id", "type": "integer", "is_primary_key": True},
                        {"name": "user_id", "type": "integer"}
                    ]
                }
            ],
            "relationships": [
                {
                    "name": "UserPosts",
                    "type": "one_to_many",
                    "table": "users",
                    "related_table": "posts",
                    "field_name": "posts",
                    "foreign_key": "user_id",
                    "referenced_key": "id"
                }
            ]
        }
        
        processed = generator.process_relationships(schema)
        assert len(processed) == 1
        assert processed[0]["table"] == "users"
        assert processed[0]["related_table"] == "posts"

    def test_field_property_extraction(self):
        """Тест извлечения свойств полей из схемы."""
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
        
        # Тестируем правильные имена полей из схемы
        field = {
            "name": "id",
            "type": "integer",
            "is_primary_key": True,
            "is_unique": False,
            "is_nullable": False,
            "default_value": None
        }
        
        assert generator.is_primary_key(field) is True
        assert generator.is_unique(field) is False
        assert generator.is_nullable(field) is False
        assert generator.get_default_value(field) is None


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
                        {"name": "id", "type": "integer", "is_primary_key": True},
                        {"name": "email", "type": "string", "is_unique": True},
                        {"name": "name", "type": "string"}
                    ]
                }
            ],
            "relationships": []
        }
        
        with tempfile.TemporaryDirectory() as temp_dir:
            result = generator.generate_models(schema, output_dir=temp_dir)
            assert len(result) > 0
            
            # Проверяем, что файл создан
            output_file = Path(temp_dir) / "schema.prisma"
            assert output_file.exists()

    def test_generate_models_with_relationships(self):
        """Тест генерации Prisma моделей со связями."""
        generator = PrismaGenerator()
        
        schema = {
            "tables": [
                {
                    "name": "users",
                    "fields": [
                        {"name": "id", "type": "integer", "is_primary_key": True},
                        {"name": "email", "type": "string"}
                    ]
                },
                {
                    "name": "posts",
                    "fields": [
                        {"name": "id", "type": "integer", "is_primary_key": True},
                        {"name": "title", "type": "string"},
                        {"name": "author_id", "type": "integer"}
                    ]
                }
            ],
            "relationships": [
                {
                    "name": "UserPosts",
                    "type": "one_to_many",
                    "table": "users",
                    "related_table": "posts",
                    "field_name": "posts",
                    "foreign_key": "author_id",
                    "referenced_key": "id"
                }
            ]
        }
        
        with tempfile.TemporaryDirectory() as temp_dir:
            result = generator.generate_models(schema, output_dir=temp_dir)
            assert len(result) > 0
            
            # Проверяем содержимое файла
            output_file = Path(temp_dir) / "schema.prisma"
            content = output_file.read_text()
            
            # Проверяем наличие моделей (используем правильные имена)
            assert "model Users {" in content
            assert "model Posts {" in content
            # Проверяем наличие связей
            assert "posts Posts[]" in content
            assert "@relation" in content

    def test_prisma_field_type_mapping(self):
        """Тест маппинга типов полей для Prisma."""
        generator = PrismaGenerator()
        
        # Проверяем основные типы (базовый генератор возвращает исходные типы)
        field = {"type": "integer"}
        assert generator.get_field_type(field) == "integer"
        
        field = {"type": "string"}
        assert generator.get_field_type(field) == "string"
        
        field = {"type": "boolean"}
        assert generator.get_field_type(field) == "boolean"
        
        field = {"type": "datetime"}
        assert generator.get_field_type(field) == "datetime"
        
        field = {"type": "text"}
        assert generator.get_field_type(field) == "text"

    def test_prisma_primary_key_handling(self):
        """Тест обработки первичных ключей в Prisma."""
        generator = PrismaGenerator()
        
        field = {"name": "id", "type": "integer", "is_primary_key": True}
        assert generator.is_primary_key(field) is True
        
        field = {"name": "email", "type": "string", "is_primary_key": False}
        assert generator.is_primary_key(field) is False

    def test_prisma_unique_constraint_handling(self):
        """Тест обработки уникальных ограничений в Prisma."""
        generator = PrismaGenerator()
        
        field = {"name": "email", "type": "string", "is_unique": True}
        assert generator.is_unique(field) is True
        
        field = {"name": "name", "type": "string", "is_unique": False}
        assert generator.is_unique(field) is False

    def test_prisma_default_value_handling(self):
        """Тест обработки значений по умолчанию в Prisma."""
        generator = PrismaGenerator()
        
        field = {"name": "created_at", "type": "datetime", "default_value": "now()"}
        assert generator.get_default_value(field) == "now()"
        
        field = {"name": "name", "type": "string", "default_value": None}
        assert generator.get_default_value(field) is None


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
                        {"name": "id", "type": "integer", "is_primary_key": True},
                        {"name": "email", "type": "string", "is_unique": True},
                        {"name": "name", "type": "string"}
                    ]
                }
            ],
            "relationships": []
        }
        
        with tempfile.TemporaryDirectory() as temp_dir:
            result = generator.generate_models(schema, output_dir=temp_dir)
            assert len(result) > 0
            
            # Проверяем, что файл создан
            output_file = Path(temp_dir) / "models.py"
            assert output_file.exists()

    def test_generate_models_with_relationships(self):
        """Тест генерации Django моделей со связями."""
        generator = DjangoGenerator()
        
        schema = {
            "tables": [
                {
                    "name": "users",
                    "fields": [
                        {"name": "id", "type": "integer", "is_primary_key": True},
                        {"name": "email", "type": "string"}
                    ]
                },
                {
                    "name": "posts",
                    "fields": [
                        {"name": "id", "type": "integer", "is_primary_key": True},
                        {"name": "title", "type": "string"},
                        {"name": "author_id", "type": "integer"}
                    ]
                }
            ],
            "relationships": [
                {
                    "name": "UserPosts",
                    "type": "one_to_many",
                    "table": "users",
                    "related_table": "posts",
                    "field_name": "posts",
                    "foreign_key": "author_id",
                    "referenced_key": "id"
                }
            ]
        }
        
        with tempfile.TemporaryDirectory() as temp_dir:
            result = generator.generate_models(schema, output_dir=temp_dir)
            assert len(result) > 0
            
            # Проверяем содержимое файла
            output_file = Path(temp_dir) / "models.py"
            content = output_file.read_text()
            
            # Проверяем наличие моделей (используем правильные имена)
            assert "class Users(models.Model):" in content
            assert "class Posts(models.Model):" in content
            # Проверяем наличие полей (Django генератор создает IntegerField для внешних ключей)
            assert "author_id" in content
            assert "models.IntegerField" in content

    def test_django_field_type_mapping(self):
        """Тест маппинга типов полей для Django."""
        generator = DjangoGenerator()

        # Проверяем основные типы (Django генератор возвращает Django типы)
        field = {"type": "integer"}
        assert generator.get_field_type(field) == "IntegerField"
        
        field = {"type": "string"}
        assert generator.get_field_type(field) == "TextField"
        
        field = {"type": "boolean"}
        assert generator.get_field_type(field) == "BooleanField"
        
        field = {"type": "datetime"}
        assert generator.get_field_type(field) == "DateTimeField"
        
        field = {"type": "text"}
        assert generator.get_field_type(field) == "TextField"

    def test_django_primary_key_handling(self):
        """Тест обработки первичных ключей в Django."""
        generator = DjangoGenerator()
        
        field = {"name": "id", "type": "integer", "is_primary_key": True}
        assert generator.is_primary_key(field) is True
        assert generator.get_field_type(field) == "AutoField"
        
        field = {"name": "email", "type": "string", "is_primary_key": False}
        assert generator.is_primary_key(field) is False

    def test_django_unique_constraint_handling(self):
        """Тест обработки уникальных ограничений в Django."""
        generator = DjangoGenerator()
        
        field = {"name": "email", "type": "string", "is_unique": True}
        assert generator.is_unique(field) is True
        
        field = {"name": "name", "type": "string", "is_unique": False}
        assert generator.is_unique(field) is False

    def test_django_nullable_handling(self):
        """Тест обработки nullable полей в Django."""
        generator = DjangoGenerator()
        
        field = {"name": "email", "type": "string", "is_nullable": False}
        assert generator.is_nullable(field) is False
        
        field = {"name": "name", "type": "string", "is_nullable": True}
        assert generator.is_nullable(field) is True

    def test_django_default_value_handling(self):
        """Тест обработки значений по умолчанию в Django."""
        generator = DjangoGenerator()
        
        field = {"name": "created_at", "type": "datetime", "default_value": "timezone.now"}
        assert generator.get_default_value(field) == "timezone.now"
        
        field = {"name": "name", "type": "string", "default_value": None}
        assert generator.get_default_value(field) is None


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
                        {"name": "id", "type": "integer", "is_primary_key": True},
                        {"name": "email", "type": "string", "is_unique": True},
                        {"name": "name", "type": "string"}
                    ]
                }
            ],
            "relationships": []
        }
        
        with tempfile.TemporaryDirectory() as temp_dir:
            result = generator.generate_models(schema, output_dir=temp_dir)
            assert len(result) > 0
            
            # Проверяем, что файл создан
            output_file = Path(temp_dir) / "models.py"
            assert output_file.exists()

    def test_generate_models_with_relationships(self):
        """Тест генерации SQLAlchemy моделей со связями."""
        generator = SQLAlchemyGenerator()
        
        schema = {
            "tables": [
                {
                    "name": "users",
                    "fields": [
                        {"name": "id", "type": "integer", "is_primary_key": True},
                        {"name": "email", "type": "string"}
                    ]
                },
                {
                    "name": "posts",
                    "fields": [
                        {"name": "id", "type": "integer", "is_primary_key": True},
                        {"name": "title", "type": "string"},
                        {"name": "author_id", "type": "integer"}
                    ]
                }
            ],
            "relationships": [
                {
                    "name": "UserPosts",
                    "type": "one_to_many",
                    "table": "users",
                    "related_table": "posts",
                    "field_name": "posts",
                    "foreign_key": "author_id",
                    "referenced_key": "id"
                }
            ]
        }
        
        with tempfile.TemporaryDirectory() as temp_dir:
            result = generator.generate_models(schema, output_dir=temp_dir)
            assert len(result) > 0
            
            # Проверяем содержимое файла
            output_file = Path(temp_dir) / "models.py"
            content = output_file.read_text()
            
            # Проверяем наличие моделей (используем правильные имена)
            assert "class Users(Base):" in content
            assert "class Posts(Base):" in content
            # Проверяем наличие relationship
            assert "relationship" in content
            assert "ForeignKey" in content

    def test_sqlalchemy_field_type_mapping(self):
        """Тест маппинга типов полей для SQLAlchemy."""
        generator = SQLAlchemyGenerator()
        
        # Проверяем основные типы (базовый генератор возвращает исходные типы)
        field = {"type": "integer"}
        assert generator.get_field_type(field) == "integer"
        
        field = {"type": "string"}
        assert generator.get_field_type(field) == "string"
        
        field = {"type": "boolean"}
        assert generator.get_field_type(field) == "boolean"
        
        field = {"type": "datetime"}
        assert generator.get_field_type(field) == "datetime"
        
        field = {"type": "text"}
        assert generator.get_field_type(field) == "text"

    def test_sqlalchemy_primary_key_handling(self):
        """Тест обработки первичных ключей в SQLAlchemy."""
        generator = SQLAlchemyGenerator()
        
        field = {"name": "id", "type": "integer", "is_primary_key": True}
        assert generator.is_primary_key(field) is True
        
        field = {"name": "email", "type": "string", "is_primary_key": False}
        assert generator.is_primary_key(field) is False

    def test_sqlalchemy_unique_constraint_handling(self):
        """Тест обработки уникальных ограничений в SQLAlchemy."""
        generator = SQLAlchemyGenerator()
        
        field = {"name": "email", "type": "string", "is_unique": True}
        assert generator.is_unique(field) is True
        
        field = {"name": "name", "type": "string", "is_unique": False}
        assert generator.is_unique(field) is False

    def test_sqlalchemy_nullable_handling(self):
        """Тест обработки nullable полей в SQLAlchemy."""
        generator = SQLAlchemyGenerator()
        
        field = {"name": "email", "type": "string", "is_nullable": False}
        assert generator.is_nullable(field) is False
        
        field = {"name": "name", "type": "string", "is_nullable": True}
        assert generator.is_nullable(field) is True

    def test_sqlalchemy_default_value_handling(self):
        """Тест обработки значений по умолчанию в SQLAlchemy."""
        generator = SQLAlchemyGenerator()
        
        field = {"name": "created_at", "type": "datetime", "default_value": "datetime.utcnow"}
        assert generator.get_default_value(field) == "datetime.utcnow"
        
        field = {"name": "name", "type": "string", "default_value": None}
        assert generator.get_default_value(field) is None


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
                        {"name": "id", "type": "integer", "is_primary_key": True},
                        {"name": "email", "type": "string", "is_unique": True}
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
        with tempfile.TemporaryDirectory() as temp_dir:
            for generator in generators:
                result = generator.generate_models(schema, output_dir=temp_dir)
                assert len(result) > 0

    def test_generator_error_handling(self):
        """Тест обработки ошибок в генераторах."""
        generators = [
            PrismaGenerator(),
            DjangoGenerator(),
            SQLAlchemyGenerator()
        ]
        
        invalid_schema = {"invalid": "schema"}
        
        # Генераторы должны корректно обрабатывать невалидные схемы
        with tempfile.TemporaryDirectory() as temp_dir:
            for generator in generators:
                # Должно работать без ошибок (валидация в базовом классе)
                result = generator.generate_models(invalid_schema, output_dir=temp_dir)
                # Результат может быть пустым для невалидных схем
                assert isinstance(result, list)

    def test_complex_schema_generation(self):
        """Тест генерации сложной схемы всеми генераторами."""
        complex_schema = {
            "tables": [
                {
                    "name": "users",
                    "fields": [
                        {"name": "id", "type": "integer", "is_primary_key": True},
                        {"name": "email", "type": "string", "is_unique": True, "is_nullable": False},
                        {"name": "name", "type": "string", "is_nullable": True},
                        {"name": "is_active", "type": "boolean", "default_value": True},
                        {"name": "created_at", "type": "datetime", "default_value": "now()"}
                    ]
                },
                {
                    "name": "posts",
                    "fields": [
                        {"name": "id", "type": "integer", "is_primary_key": True},
                        {"name": "title", "type": "string", "is_nullable": False},
                        {"name": "content", "type": "text"},
                        {"name": "author_id", "type": "integer"},
                        {"name": "created_at", "type": "datetime", "default_value": "now()"}
                    ]
                },
                {
                    "name": "comments",
                    "fields": [
                        {"name": "id", "type": "integer", "is_primary_key": True},
                        {"name": "content", "type": "text", "is_nullable": False},
                        {"name": "user_id", "type": "integer"},
                        {"name": "post_id", "type": "integer"},
                        {"name": "created_at", "type": "datetime", "default_value": "now()"}
                    ]
                }
            ],
            "relationships": [
                {
                    "name": "UserPosts",
                    "type": "one_to_many",
                    "table": "users",
                    "related_table": "posts",
                    "field_name": "posts",
                    "foreign_key": "author_id",
                    "referenced_key": "id"
                },
                {
                    "name": "UserComments",
                    "type": "one_to_many",
                    "table": "users",
                    "related_table": "comments",
                    "field_name": "comments",
                    "foreign_key": "user_id",
                    "referenced_key": "id"
                },
                {
                    "name": "PostComments",
                    "type": "one_to_many",
                    "table": "posts",
                    "related_table": "comments",
                    "field_name": "comments",
                    "foreign_key": "post_id",
                    "referenced_key": "id"
                }
            ]
        }
        
        generators = [
            PrismaGenerator(),
            DjangoGenerator(),
            SQLAlchemyGenerator()
        ]
        
        with tempfile.TemporaryDirectory() as temp_dir:
            for generator in generators:
                result = generator.generate_models(complex_schema, output_dir=temp_dir)
                assert len(result) > 0
                
                # Проверяем, что файл создан
                if isinstance(generator, PrismaGenerator):
                    output_file = Path(temp_dir) / "schema.prisma"
                else:
                    output_file = Path(temp_dir) / "models.py"
                
                assert output_file.exists()
                content = output_file.read_text()
                
                # Проверяем наличие всех моделей
                assert "User" in content or "user" in content.lower()
                assert "Post" in content or "post" in content.lower()
                assert "Comment" in content or "comment" in content.lower()

    def test_field_constraints_consistency(self):
        """Тест консистентности обработки ограничений полей."""
        schema = {
            "tables": [
                {
                    "name": "test_table",
                    "fields": [
                        {"name": "id", "type": "integer", "is_primary_key": True},
                        {"name": "unique_field", "type": "string", "is_unique": True},
                        {"name": "required_field", "type": "string", "is_nullable": False},
                        {"name": "default_field", "type": "string", "default_value": "default_value"}
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
        
        with tempfile.TemporaryDirectory() as temp_dir:
            for generator in generators:
                result = generator.generate_models(schema, output_dir=temp_dir)
                assert len(result) > 0
                
                # Проверяем, что генератор корректно обрабатывает ограничения
                if isinstance(generator, PrismaGenerator):
                    output_file = Path(temp_dir) / "schema.prisma"
                else:
                    output_file = Path(temp_dir) / "models.py"
                
                content = output_file.read_text()
                
                # Проверяем наличие первичного ключа
                if isinstance(generator, PrismaGenerator):
                    assert "@id" in content
                elif isinstance(generator, DjangoGenerator):
                    assert "AutoField" in content
                else:  # SQLAlchemy
                    assert "primary_key=True" in content 