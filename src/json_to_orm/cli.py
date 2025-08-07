"""
CLI interface for JSON-to-ORM.

This module provides command line interface for generating ORM models
from JSON data schemas.
"""

import sys
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

from .core import JSONToORM
from .utils.logger import setup_logger, get_logger

# Create Typer instance
app = typer.Typer(
    name="json-to-orm",
    help="CLI utility for generating ORM models from JSON schemas",
    add_completion=False,
)

# Create console for beautiful output
console = Console()

# Setup logging
setup_logger()
logger = get_logger(__name__)


@app.command()
def generate(
    input_file: Path = typer.Argument(
        ...,
        help="Path to JSON file with data schema",
        exists=True,
        file_okay=True,
        dir_okay=False,
    ),
    output_dir: Path = typer.Argument(
        ...,
        help="Directory to save generated models",
    ),
    format: str = typer.Option(
        "prisma",
        "--format",
        "-f",
        help="Generation format (prisma, django, sqlalchemy)",
        case_sensitive=False,
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        help="Verbose output",
    ),
) -> None:
    """
    Generates ORM models from JSON data schema.

    Examples:
        json-to-orm generate schema.json models/ --format prisma
        json-to-orm generate schema.json models/ -f django -v
    """
    try:
        if verbose:
            console.print(
                f"[bold blue]Generating models in {format.upper()} format[/bold blue]"
            )
            console.print(f"Input file: {input_file}")
            console.print(f"Output directory: {output_dir}")

        # Create converter instance
        converter = JSONToORM()

        # Generate models
        result = converter.generate(
            input_file=str(input_file),
            output_dir=str(output_dir),
            format=format.lower(),
            verbose=verbose,
        )

        if verbose:
            console.print(f"[bold green]✓ Models generated successfully![/bold green]")
            console.print(f"Files created: {result.files_created}")
            console.print(f"Execution time: {result.execution_time:.2f}s")
        else:
            console.print(
                f"[bold green]✓ Models generated successfully in {output_dir}[/bold green]"
            )

    except Exception as e:
        logger.error(f"Error generating models: {e}")
        console.print(f"[bold red]✗ Error: {e}[/bold red]")
        sys.exit(1)


@app.command()
def validate(
    input_file: Path = typer.Argument(
        ...,
        help="Path to JSON file for validation",
        exists=True,
        file_okay=True,
        dir_okay=False,
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        help="Verbose output",
    ),
) -> None:
    """
    Validates JSON data schema.

    Examples:
        json-to-orm validate schema.json
        json-to-orm validate schema.json -v
    """
    try:
        if verbose:
            console.print(f"[bold blue]Validating data schema[/bold blue]")
            console.print(f"File: {input_file}")

        # Create converter instance
        converter = JSONToORM()

        # Validate schema
        validation_result = converter.validate(str(input_file))

        if validation_result.is_valid:
            if verbose:
                console.print(f"[bold green]✓ Schema is valid![/bold green]")
                console.print(f"Number of tables: {validation_result.table_count}")
                console.print(
                    f"Number of relationships: {validation_result.relationship_count}"
                )
            else:
                console.print(f"[bold green]✓ Schema is valid[/bold green]")
        else:
            console.print(f"[bold red]✗ Schema contains errors:[/bold red]")
            for error in validation_result.errors:
                console.print(f"  - {error}")
            sys.exit(1)

    except Exception as e:
        logger.error(f"Error validating schema: {e}")
        console.print(f"[bold red]✗ Error: {e}[/bold red]")
        sys.exit(1)


@app.command()
def list_formats() -> None:
    """
    Shows list of supported generation formats.

    Examples:
        json-to-orm list-formats
    """
    try:
        console.print("[bold blue]Supported generation formats:[/bold blue]")

        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Format", style="cyan")
        table.add_column("Description", style="white")
        table.add_column("File Extension", style="green")

        # Create converter instance to get format information
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
        logger.error(f"Error getting format list: {e}")
        console.print(f"[bold red]✗ Error: {e}[/bold red]")
        sys.exit(1)


@app.command()
def version() -> None:
    """
    Shows utility version.

    Examples:
        json-to-orm version
    """
    from . import __version__

    console.print(f"[bold blue]JSON-to-ORM version {__version__}[/bold blue]")


def main() -> None:
    """
    Main CLI function.
    """
    try:
        app()
    except KeyboardInterrupt:
        console.print("\n[yellow]Operation interrupted by user[/yellow]")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        console.print(f"[bold red]Critical error: {e}[/bold red]")
        sys.exit(1)


if __name__ == "__main__":
    main()
