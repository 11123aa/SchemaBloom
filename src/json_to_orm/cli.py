"""
CLI интерфейс для JSON-to-ORM.

Этот модуль предоставляет командную строку для генерации ORM моделей
из JSON-схем данных.
"""

import sys
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

from .core import JSONToORM
from .utils.logger import setup_logger, get_logger

# Создание экземпляра Typer
app = typer.Typer(
    name="json-to-orm",
    help="CLI-утилита для генерации ORM моделей из JSON-схем",
    add_completion=False,
)

# Создание консоли для красивого вывода
console = Console()

# Настройка логирования
setup_logger()
logger = get_logger(__name__)


@app.command()
def generate(
    input_file: Path = typer.Argument(
        ...,
        help="Путь к JSON-файлу со схемой данных",
        exists=True,
        file_okay=True,
        dir_okay=False,
    ),
    output_dir: Path = typer.Argument(
        ...,
        help="Директория для сохранения сгенерированных моделей",
    ),
    format: str = typer.Option(
        "prisma",
        "--format",
        "-f",
        help="Формат генерации (prisma, django, sqlalchemy)",
        case_sensitive=False,
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        help="Подробный вывод",
    ),
) -> None:
    """
    Генерирует ORM модели из JSON-схемы данных.

    Примеры:
        json-to-orm generate schema.json models/ --format prisma
        json-to-orm generate schema.json models/ -f django -v
    """
    try:
        if verbose:
            console.print(
                f"[bold blue]Генерация моделей в формате {format.upper()}[/bold blue]"
            )
            console.print(f"Входной файл: {input_file}")
            console.print(f"Выходная директория: {output_dir}")

        # Создание экземпляра конвертера
        converter = JSONToORM()

        # Генерация моделей
        result = converter.generate(
            input_file=str(input_file),
            output_dir=str(output_dir),
            format=format.lower(),
            verbose=verbose,
        )

        if verbose:
            console.print(f"[bold green]✓ Модели успешно сгенерированы![/bold green]")
            console.print(f"Создано файлов: {result.files_created}")
            console.print(f"Время выполнения: {result.execution_time:.2f}с")
        else:
            console.print(
                f"[bold green]✓ Модели успешно сгенерированы в {output_dir}[/bold green]"
            )

    except Exception as e:
        logger.error(f"Ошибка при генерации моделей: {e}")
        console.print(f"[bold red]✗ Ошибка: {e}[/bold red]")
        sys.exit(1)


@app.command()
def validate(
    input_file: Path = typer.Argument(
        ...,
        help="Путь к JSON-файлу для валидации",
        exists=True,
        file_okay=True,
        dir_okay=False,
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        help="Подробный вывод",
    ),
) -> None:
    """
    Валидирует JSON-схему данных.

    Примеры:
        json-to-orm validate schema.json
        json-to-orm validate schema.json -v
    """
    try:
        if verbose:
            console.print(f"[bold blue]Валидация схемы данных[/bold blue]")
            console.print(f"Файл: {input_file}")

        # Создание экземпляра конвертера
        converter = JSONToORM()

        # Валидация схемы
        validation_result = converter.validate(str(input_file))

        if validation_result.is_valid:
            if verbose:
                console.print(f"[bold green]✓ Схема валидна![/bold green]")
                console.print(f"Количество таблиц: {validation_result.table_count}")
                console.print(
                    f"Количество связей: {validation_result.relationship_count}"
                )
            else:
                console.print(f"[bold green]✓ Схема валидна[/bold green]")
        else:
            console.print(f"[bold red]✗ Схема содержит ошибки:[/bold red]")
            for error in validation_result.errors:
                console.print(f"  - {error}")
            sys.exit(1)

    except Exception as e:
        logger.error(f"Ошибка при валидации схемы: {e}")
        console.print(f"[bold red]✗ Ошибка: {e}[/bold red]")
        sys.exit(1)


@app.command()
def list_formats() -> None:
    """
    Показывает список поддерживаемых форматов генерации.

    Примеры:
        json-to-orm list-formats
    """
    try:
        console.print("[bold blue]Поддерживаемые форматы генерации:[/bold blue]")

        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Формат", style="cyan")
        table.add_column("Описание", style="white")
        table.add_column("Расширение файла", style="green")

        # Создание экземпляра конвертера для получения информации о форматах
        converter = JSONToORM()
        
        formats = []
        for format_name in converter.get_supported_formats():
            format_info = converter.get_format_info(format_name)
            if format_info:
                formats.append((
                    format_name,
                    format_info["description"],
                    format_info["extension"]
                ))

        for format_name, description, extension in formats:
            table.add_row(format_name, description, extension)

        console.print(table)

    except Exception as e:
        logger.error(f"Ошибка при получении списка форматов: {e}")
        console.print(f"[bold red]✗ Ошибка: {e}[/bold red]")
        sys.exit(1)


@app.command()
def version() -> None:
    """
    Показывает версию утилиты.

    Примеры:
        json-to-orm version
    """
    from . import __version__

    console.print(f"[bold blue]JSON-to-ORM версия {__version__}[/bold blue]")


def main() -> None:
    """
    Главная функция CLI.
    """
    try:
        app()
    except KeyboardInterrupt:
        console.print("\n[yellow]Операция прервана пользователем[/yellow]")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Неожиданная ошибка: {e}")
        console.print(f"[bold red]Критическая ошибка: {e}[/bold red]")
        sys.exit(1)


if __name__ == "__main__":
    main()
