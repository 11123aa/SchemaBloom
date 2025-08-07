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


@app.command()
def interactive():
    """Interactive schema creation mode"""
    from rich.console import Console
    from rich.prompt import Prompt, Confirm
    from rich.table import Table
    
    console = Console()
    console.print("[bold blue]SchemaBloom Interactive Mode[/bold blue]")
    console.print("Create your database schema step by step\n")
    
    # TODO: Implement interactive schema creation
    console.print("[yellow]Interactive mode coming soon![/yellow]")
    console.print("This will allow you to create schemas step by step with validation.")

@app.command()
def watch(
    schema_file: str = typer.Argument(..., help="Path to JSON schema file"),
    output_dir: str = typer.Argument(..., help="Output directory for generated models"),
    format: str = typer.Option("prisma", "--format", "-f", help="Output format (prisma, django, sqlalchemy)"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output")
):
    """Watch schema file for changes and regenerate models automatically"""
    from rich.console import Console
    from rich.live import Live
    from rich.panel import Panel
    import time
    import os
    
    console = Console()
    console.print(f"[bold blue]Watching {schema_file} for changes...[/bold blue]")
    console.print(f"Output format: {format}")
    console.print(f"Output directory: {output_dir}")
    console.print("Press Ctrl+C to stop\n")
    
    last_modified = 0
    
    try:
        while True:
            if os.path.exists(schema_file):
                current_modified = os.path.getmtime(schema_file)
                if current_modified > last_modified:
                    console.print(f"[green]Schema changed, regenerating models...[/green]")
                    try:
                        generate(schema_file, output_dir, format, verbose)
                        console.print(f"[green]✓ Models regenerated successfully![/green]")
                        last_modified = current_modified
                    except Exception as e:
                        console.print(f"[red]✗ Error regenerating models: {e}[/red]")
            
            time.sleep(1)
    except KeyboardInterrupt:
        console.print("\n[yellow]Stopped watching for changes[/yellow]")

@app.command()
def export(
    schema_file: str = typer.Argument(..., help="Path to JSON schema file"),
    output_format: str = typer.Option("yaml", "--format", "-f", help="Export format (yaml, xml, sql)"),
    output_file: str = typer.Option(None, "--output", "-o", help="Output file path")
):
    """Export schema to different formats"""
    from rich.console import Console
    
    console = Console()
    console.print(f"[bold blue]Exporting schema to {output_format.upper()} format[/bold blue]")
    
    # TODO: Implement schema export functionality
    console.print("[yellow]Export functionality coming soon![/yellow]")
    console.print(f"Will export {schema_file} to {output_format} format")

@app.command()
def validate_schema(
    schema_file: str = typer.Argument(..., help="Path to JSON schema file"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose validation output")
):
    """Validate JSON schema with detailed feedback"""
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from json_to_orm.parser.json_parser import JSONParser
    from json_to_orm.parser.validator import SchemaValidator
    
    console = Console()
    
    try:
        # Parse and validate schema
        parser = JSONParser()
        validator = SchemaValidator()
        
        console.print(f"[bold blue]Validating schema: {schema_file}[/bold blue]\n")
        
        # Parse JSON
        schema_data = parser.parse_file(schema_file)
        console.print("[green]✓ JSON parsing successful[/green]")
        
        # Validate schema
        validation_result = validator.validate_schema(schema_data)
        
        if validation_result.is_valid:
            console.print("[green]✓ Schema validation successful[/green]")
            
            if verbose:
                # Show detailed validation info
                table = Table(title="Schema Summary")
                table.add_column("Component", style="cyan")
                table.add_column("Count", style="magenta")
                table.add_column("Status", style="green")
                
                table.add_row("Tables", str(len(schema_data.get("tables", []))), "✓ Valid")
                table.add_row("Relationships", str(len(schema_data.get("relationships", []))), "✓ Valid")
                table.add_row("Fields", str(sum(len(t.get("fields", [])) for t in schema_data.get("tables", []))), "✓ Valid")
                
                console.print(table)
        else:
            console.print("[red]✗ Schema validation failed[/red]")
            
            if verbose:
                for error in validation_result.errors:
                    console.print(f"[red]Error: {error}[/red]")
                    
    except Exception as e:
        console.print(f"[red]✗ Validation error: {e}[/red]")

@app.command()
def list_formats():
    """List all supported output formats with descriptions"""
    from rich.console import Console
    from rich.table import Table
    
    console = Console()
    
    table = Table(title="Supported Output Formats")
    table.add_column("Format", style="cyan", no_wrap=True)
    table.add_column("Description", style="white")
    table.add_column("Status", style="green")
    
    formats = [
        ("prisma", "Prisma ORM schema with client and datasource configuration", "✓ Ready"),
        ("django", "Django ORM models with relationships and Meta classes", "✓ Ready"),
        ("sqlalchemy", "SQLAlchemy declarative models with relationships", "✓ Ready"),
        ("sequelize", "Sequelize ORM for Node.js (JavaScript/TypeScript)", "🔄 Planned"),
        ("typeorm", "TypeORM for TypeScript projects", "🔄 Planned"),
        ("gorm", "GORM for Go projects", "📋 Future"),
        ("entity-framework", "Entity Framework Core for .NET", "📋 Future"),
    ]
    
    for format_name, description, status in formats:
        table.add_row(format_name, description, status)
    
    console.print(table)


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
