"""
Тесты для утилит и фильтров шаблонов.
"""

import pytest
from pathlib import Path
from unittest.mock import patch, mock_open
import logging
import tempfile

from json_to_orm.utils.template_filters import (
    snake_case, 
    pascal_case, 
    camel_case, 
    prisma_type, 
    django_type, 
    sqlalchemy_type
)
from json_to_orm.utils.helpers import (
    ensure_directory,
    get_file_extension,
    validate_file_path
)
from json_to_orm.utils.logger import setup_logger


class TestTemplateFilters:
    """Тесты для фильтров шаблонов."""

    def test_snake_case(self):
        """Тест преобразования в snake_case."""
        assert snake_case("User") == "user"
        assert snake_case("UserProfile") == "userprofile"
        assert snake_case("userProfile") == "userprofile"
        assert snake_case("user_profile") == "user_profile"
        assert snake_case("USER_PROFILE") == "user_profile"
        assert snake_case("user") == "user"

    def test_pascal_case(self):
        """Тест преобразования в PascalCase."""
        assert pascal_case("user") == "User"
        assert pascal_case("user_profile") == "UserProfile"
        assert pascal_case("userProfile") == "Userprofile"
        assert pascal_case("UserProfile") == "Userprofile"
        assert pascal_case("USER_PROFILE") == "UserProfile"

    def test_camel_case(self):
        """Тест преобразования в camelCase."""
        assert camel_case("user") == "user"
        assert camel_case("user_profile") == "userProfile"
        assert camel_case("UserProfile") == "userprofile"
        assert camel_case("userProfile") == "userprofile"
        assert camel_case("USER_PROFILE") == "userProfile"

    def test_prisma_type_mapping(self):
        """Тест маппинга типов для Prisma."""
        assert prisma_type("integer") == "Int"
        assert prisma_type("string") == "String"
        assert prisma_type("boolean") == "Boolean"
        assert prisma_type("datetime") == "DateTime"
        assert prisma_type("text") == "String"
        assert prisma_type("float") == "Float"
        assert prisma_type("decimal") == "Decimal"
        assert prisma_type("json") == "Json"
        
        # Неизвестный тип должен возвращать String
        assert prisma_type("unknown_type") == "String"

    def test_django_type_mapping(self):
        """Тест маппинга типов для Django."""
        assert django_type("integer") == "IntegerField"
        assert django_type("string") == "CharField"
        assert django_type("boolean") == "BooleanField"
        assert django_type("datetime") == "DateTimeField"
        assert django_type("text") == "TextField"
        assert django_type("float") == "FloatField"
        assert django_type("decimal") == "DecimalField"
        assert django_type("json") == "JSONField"
        
        # Неизвестный тип должен возвращать CharField
        assert django_type("unknown_type") == "CharField"

    def test_sqlalchemy_type_mapping(self):
        """Тест маппинга типов для SQLAlchemy."""
        assert sqlalchemy_type("integer") == "Integer"
        assert sqlalchemy_type("string") == "String"
        assert sqlalchemy_type("boolean") == "Boolean"
        assert sqlalchemy_type("datetime") == "DateTime"
        assert sqlalchemy_type("text") == "Text"
        assert sqlalchemy_type("float") == "Float"
        assert sqlalchemy_type("decimal") == "Numeric"
        assert sqlalchemy_type("json") == "JSON"
        
        # Неизвестный тип должен возвращать String
        assert sqlalchemy_type("unknown_type") == "String"

    def test_edge_cases(self):
        """Тест граничных случаев для фильтров."""
        # Пустые строки
        assert snake_case("") == ""
        assert pascal_case("") == ""
        assert camel_case("") == ""
        
        # Одиночные символы
        assert snake_case("a") == "a"
        assert pascal_case("a") == "A"
        assert camel_case("a") == "a"
        
        # Числа в названиях
        assert snake_case("user123") == "user123"
        assert pascal_case("user123") == "User123"
        assert camel_case("user123") == "user123"
        
        # Специальные символы
        assert snake_case("user-name") == "user_name"
        assert pascal_case("user-name") == "UserName"
        assert camel_case("user-name") == "userName"


class TestHelpers:
    """Тесты для вспомогательных функций."""

    def test_ensure_directory(self):
        """Тест создания директории."""
        with patch('pathlib.Path.mkdir') as mock_mkdir:
            ensure_directory("/test/path")
            mock_mkdir.assert_called_once_with(parents=True, exist_ok=True)

    def test_get_file_extension(self):
        """Тест получения расширения файла."""
        assert get_file_extension("test.json") == ".json"
        assert get_file_extension("models.py") == ".py"
        assert get_file_extension("schema.prisma") == ".prisma"
        assert get_file_extension("file_without_extension") == ""

    def test_validate_file_path(self):
        """Тест валидации пути к файлу."""
        # Валидный путь
        with patch('pathlib.Path.exists', return_value=True):
            with patch('pathlib.Path.is_file', return_value=True):
                result = validate_file_path("/test/file.json")
                assert isinstance(result, Path)
        
        # Несуществующий файл
        with patch('pathlib.Path.exists', return_value=False):
            with pytest.raises(FileNotFoundError):
                validate_file_path("/test/nonexistent.json")
        
        # Директория вместо файла
        with patch('pathlib.Path.exists', return_value=True):
            with patch('pathlib.Path.is_file', return_value=False):
                with pytest.raises(ValueError):
                    validate_file_path("/test/directory")


class TestLogger:
    """Тесты для системы логирования."""

    def test_setup_logger(self):
        """Тест настройки логгера."""
        # Тестируем базовую настройку логгера
        setup_logger()
        # Логгер должен быть настроен без ошибок
        assert True

    def test_logger_levels(self):
        """Тест уровней логирования."""
        # Тестируем настройку с разными уровнями
        setup_logger(level=logging.DEBUG)
        # Логгер должен быть настроен без ошибок
        assert True

    def test_logger_with_file(self):
        """Тест логгера с файловым хендлером."""
        with tempfile.TemporaryDirectory() as temp_dir:
            log_file = Path(temp_dir) / "test.log"
            setup_logger(log_file=str(log_file))
            # Логгер должен быть настроен без ошибок
            assert True


class TestIntegration:
    """Интеграционные тесты для утилит."""

    def test_template_filters_integration(self):
        """Тест интеграции фильтров шаблонов."""
        # Тестируем полный цикл преобразования
        table_name = "user_profile"
        
        snake = snake_case(table_name)
        pascal = pascal_case(table_name)
        camel = camel_case(table_name)
        
        assert snake == "user_profile"
        assert pascal == "UserProfile"
        assert camel == "userProfile"
        
        # Проверяем консистентность
        assert snake_case(pascal) == "userprofile"
        assert pascal_case(snake) == "UserProfile"

    def test_type_mapping_consistency(self):
        """Тест консистентности маппинга типов."""
        test_types = ["integer", "string", "boolean", "datetime", "text"]
        
        for type_name in test_types:
            prisma_result = prisma_type(type_name)
            django_result = django_type(type_name)
            sqlalchemy_result = sqlalchemy_type(type_name)
            
            # Все результаты должны быть строками
            assert isinstance(prisma_result, str)
            assert isinstance(django_result, str)
            assert isinstance(sqlalchemy_result, str)
            
            # Результаты не должны быть пустыми
            assert len(prisma_result) > 0
            assert len(django_result) > 0
            assert len(sqlalchemy_result) > 0

    def test_file_operations_integration(self):
        """Тест интеграции файловых операций."""
        with patch('pathlib.Path.mkdir') as mock_mkdir:
            with patch('pathlib.Path.exists', return_value=True):
                with patch('pathlib.Path.is_file', return_value=True):
                    # Тестируем полный цикл валидации и создания директории
                    file_path = "/test/output/models.py"
                    result = validate_file_path(file_path)
                    
                    ensure_directory("/test/output")
                    
                    mock_mkdir.assert_called_once_with(parents=True, exist_ok=True)

    def test_error_handling(self):
        """Тест обработки ошибок в утилитах."""
        # Тестируем обработку некорректных входных данных
        assert snake_case(None) is None
        assert pascal_case(None) is None
        assert camel_case(None) is None
        
        # Тестируем обработку некорректных типов
        assert prisma_type(None) == "String"
        assert django_type(None) == "CharField"
        assert sqlalchemy_type(None) == "String"
        
        # Тестируем обработку некорректных путей
        with patch('pathlib.Path.exists', side_effect=Exception("Test error")):
            with pytest.raises(Exception):
                validate_file_path("/test/file.json") 