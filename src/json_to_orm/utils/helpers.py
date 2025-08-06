"""
Вспомогательные функции для JSON-to-ORM.

Этот модуль содержит различные утилитарные функции для работы
с файлами, путями и другими общими операциями.
"""

import os
from pathlib import Path
from typing import Union


def validate_file_path(file_path: Union[str, Path]) -> Path:
    """
    Валидирует путь к файлу.

    Args:
        file_path: Путь к файлу

    Returns:
        Path: Валидный путь к файлу

    Raises:
        FileNotFoundError: Если файл не существует
        ValueError: Если путь не является файлом
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Файл не найден: {path}")

    if not path.is_file():
        raise ValueError(f"Путь не является файлом: {path}")

    return path


def ensure_directory(directory_path: Union[str, Path]) -> Path:
    """
    Создает директорию, если она не существует.

    Args:
        directory_path: Путь к директории

    Returns:
        Path: Путь к созданной директории
    """
    path = Path(directory_path)
    path.mkdir(parents=True, exist_ok=True)
    return path


def get_file_extension(file_path: Union[str, Path]) -> str:
    """
    Возвращает расширение файла.

    Args:
        file_path: Путь к файлу

    Returns:
        str: Расширение файла (включая точку)
    """
    return Path(file_path).suffix


def get_file_name_without_extension(file_path: Union[str, Path]) -> str:
    """
    Возвращает имя файла без расширения.

    Args:
        file_path: Путь к файлу

    Returns:
        str: Имя файла без расширения
    """
    return Path(file_path).stem


def is_json_file(file_path: Union[str, Path]) -> bool:
    """
    Проверяет, является ли файл JSON-файлом.

    Args:
        file_path: Путь к файлу

    Returns:
        bool: True, если файл имеет расширение .json
    """
    return get_file_extension(file_path).lower() == ".json"


def sanitize_filename(filename: str) -> str:
    """
    Очищает имя файла от недопустимых символов.

    Args:
        filename: Исходное имя файла

    Returns:
        str: Очищенное имя файла
    """
    # Замена недопустимых символов на подчеркивание
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, "_")

    # Удаление начальных и конечных пробелов и точек
    filename = filename.strip(" .")

    # Если имя файла пустое, используем значение по умолчанию
    if not filename:
        filename = "unnamed"

    return filename


def get_relative_path(
    base_path: Union[str, Path], target_path: Union[str, Path]
) -> str:
    """
    Возвращает относительный путь от базового пути к целевому.

    Args:
        base_path: Базовый путь
        target_path: Целевой путь

    Returns:
        str: Относительный путь
    """
    base = Path(base_path).resolve()
    target = Path(target_path).resolve()

    try:
        return str(target.relative_to(base))
    except ValueError:
        # Если пути не связаны, возвращаем абсолютный путь
        return str(target)


def create_backup(file_path: Union[str, Path], suffix: str = ".bak") -> Path:
    """
    Создает резервную копию файла.

    Args:
        file_path: Путь к файлу
        suffix: Суффикс для резервной копии

    Returns:
        Path: Путь к резервной копии
    """
    path = Path(file_path)
    backup_path = path.with_suffix(path.suffix + suffix)

    if path.exists():
        import shutil

        shutil.copy2(path, backup_path)

    return backup_path


def get_file_size(file_path: Union[str, Path]) -> int:
    """
    Возвращает размер файла в байтах.

    Args:
        file_path: Путь к файлу

    Returns:
        int: Размер файла в байтах
    """
    return Path(file_path).stat().st_size


def format_file_size(size_bytes: int) -> str:
    """
    Форматирует размер файла в читаемый вид.

    Args:
        size_bytes: Размер в байтах

    Returns:
        str: Отформатированный размер
    """
    if size_bytes == 0:
        return "0 B"

    size_names = ["B", "KB", "MB", "GB", "TB"]
    import math

    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)

    return f"{s} {size_names[i]}"
