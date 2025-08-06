"""
Модуль логирования для JSON-to-ORM.

Этот модуль предоставляет настройку и использование логирования
для отслеживания операций в рамках проекта.
"""

import logging
import sys
from pathlib import Path
from typing import Optional

# Глобальный логгер
_logger: Optional[logging.Logger] = None


def setup_logger(
    level: int = logging.INFO,
    log_file: Optional[str] = None,
    format_string: Optional[str] = None,
) -> None:
    """
    Настраивает глобальный логгер.
    
    Args:
        level: Уровень логирования
        log_file: Путь к файлу логов (опционально)
        format_string: Строка форматирования логов
    """
    global _logger
    
    if _logger is not None:
        return
    
    # Создание логгера
    _logger = logging.getLogger("json_to_orm")
    _logger.setLevel(level)
    
    # Очистка существующих обработчиков
    _logger.handlers.clear()
    
    # Настройка форматирования
    if format_string is None:
        format_string = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    formatter = logging.Formatter(format_string)
    
    # Обработчик для консоли
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    _logger.addHandler(console_handler)
    
    # Обработчик для файла (если указан)
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        _logger.addHandler(file_handler)
    
    _logger.info("Логгер настроен")


def get_logger(name: str) -> logging.Logger:
    """
    Возвращает логгер для указанного модуля.
    
    Args:
        name: Имя модуля
        
    Returns:
        logging.Logger: Настроенный логгер
    """
    if _logger is None:
        setup_logger()
    
    return logging.getLogger(f"json_to_orm.{name}")


def set_log_level(level: int) -> None:
    """
    Устанавливает уровень логирования.
    
    Args:
        level: Новый уровень логирования
    """
    if _logger is not None:
        _logger.setLevel(level)
        for handler in _logger.handlers:
            handler.setLevel(level)


def disable_logging() -> None:
    """Отключает логирование."""
    if _logger is not None:
        _logger.disabled = True


def enable_logging() -> None:
    """Включает логирование."""
    if _logger is not None:
        _logger.disabled = False 