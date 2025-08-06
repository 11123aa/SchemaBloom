"""
Основной модуль JSON-to-ORM.

Этот модуль содержит основной класс JSONToORM, который координирует
работу парсера, валидатора и генераторов.
"""

import time
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Union

from .parser import JSONParser, SchemaValidator
from .generators import BaseGenerator, PrismaGenerator, DjangoGenerator, SQLAlchemyGenerator
from .utils.logger import get_logger

logger = get_logger(__name__)


@dataclass
class GenerationResult:
    """Результат генерации моделей."""
    success: bool
    files_created: int
    execution_time: float
    output_dir: str
    errors: List[str]


@dataclass
class ValidationResult:
    """Результат валидации схемы."""
    is_valid: bool
    table_count: int
    relationship_count: int
    errors: List[str]


class JSONToORM:
    """
    Основной класс для генерации ORM моделей из JSON-схем.
    
    Этот класс координирует работу парсера, валидатора и генераторов
    для создания ORM моделей в различных форматах.
    """
    
    def __init__(self) -> None:
        """Инициализация JSONToORM."""
        self.parser = JSONParser()
        self.validator = SchemaValidator()
        self.generators: Dict[str, BaseGenerator] = {
            "prisma": PrismaGenerator(),
            "django": DjangoGenerator(),
            "sqlalchemy": SQLAlchemyGenerator(),
        }
        logger.info("JSONToORM инициализирован")
    
    def generate(
        self,
        input_file: str,
        output_dir: str,
        format: str = "prisma",
        verbose: bool = False,
    ) -> GenerationResult:
        """
        Генерирует ORM модели из JSON-схемы.
        
        Args:
            input_file: Путь к JSON-файлу со схемой
            output_dir: Директория для сохранения моделей
            format: Формат генерации (prisma, django, sqlalchemy)
            verbose: Подробный вывод
            
        Returns:
            GenerationResult: Результат генерации
            
        Raises:
            ValueError: Если формат не поддерживается
            FileNotFoundError: Если входной файл не найден
        """
        start_time = time.time()
        
        try:
            if verbose:
                logger.info(f"Начало генерации моделей в формате {format}")
            
            # Проверка формата
            if format not in self.generators:
                raise ValueError(f"Неподдерживаемый формат: {format}")
            
            # Парсинг JSON-схемы
            if verbose:
                logger.info("Парсинг JSON-схемы")
            schema = self.parser.parse(input_file)
            
            # Валидация схемы
            if verbose:
                logger.info("Валидация схемы")
            validation_result = self.validator.validate(schema)
            
            if not validation_result.is_valid:
                errors = [f"Ошибка валидации: {error}" for error in validation_result.errors]
                return GenerationResult(
                    success=False,
                    files_created=0,
                    execution_time=time.time() - start_time,
                    output_dir=output_dir,
                    errors=errors
                )
            
            # Генерация моделей
            if verbose:
                logger.info(f"Генерация моделей в формате {format}")
            generator = self.generators[format]
            files_created = generator.generate(schema, output_dir)
            
            execution_time = time.time() - start_time
            
            if verbose:
                logger.info(f"Генерация завершена. Создано файлов: {files_created}")
            
            return GenerationResult(
                success=True,
                files_created=files_created,
                execution_time=execution_time,
                output_dir=output_dir,
                errors=[]
            )
            
        except Exception as e:
            logger.error(f"Ошибка при генерации: {e}")
            return GenerationResult(
                success=False,
                files_created=0,
                execution_time=time.time() - start_time,
                output_dir=output_dir,
                errors=[str(e)]
            )
    
    def validate(self, input_file: str) -> ValidationResult:
        """
        Валидирует JSON-схему.
        
        Args:
            input_file: Путь к JSON-файлу для валидации
            
        Returns:
            ValidationResult: Результат валидации
        """
        try:
            # Парсинг JSON-схемы
            schema = self.parser.parse(input_file)
            
            # Валидация схемы
            validation_result = self.validator.validate(schema)
            
            return validation_result
            
        except Exception as e:
            logger.error(f"Ошибка при валидации: {e}")
            return ValidationResult(
                is_valid=False,
                table_count=0,
                relationship_count=0,
                errors=[str(e)]
            )
    
    def get_supported_formats(self) -> List[str]:
        """
        Возвращает список поддерживаемых форматов.
        
        Returns:
            List[str]: Список поддерживаемых форматов
        """
        return list(self.generators.keys())
    
    def get_format_info(self, format: str) -> Optional[Dict[str, str]]:
        """
        Возвращает информацию о формате.
        
        Args:
            format: Название формата
            
        Returns:
            Optional[Dict[str, str]]: Информация о формате или None
        """
        format_info = {
            "prisma": {
                "name": "Prisma Schema",
                "description": "Генерация Prisma схемы",
                "extension": ".prisma",
                "framework": "Prisma ORM"
            },
            "django": {
                "name": "Django Models",
                "description": "Генерация Django моделей",
                "extension": ".py",
                "framework": "Django ORM"
            },
            "sqlalchemy": {
                "name": "SQLAlchemy Models",
                "description": "Генерация SQLAlchemy моделей",
                "extension": ".py",
                "framework": "SQLAlchemy ORM"
            }
        }
        
        return format_info.get(format.lower()) 