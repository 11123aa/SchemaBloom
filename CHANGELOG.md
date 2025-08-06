# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-12-19

### Added
- Initial release of SchemaBloom JSON-to-ORM CLI utility
- Support for generating ORM models from JSON schemas
- Three ORM format generators:
  - **Prisma**: Full Prisma schema generation with relationships
  - **Django**: Django ORM models with Meta classes and relationships
  - **SQLAlchemy**: SQLAlchemy models with declarative base and relationships
- JSON schema validation with detailed error reporting
- CLI interface with multiple commands:
  - `generate`: Generate ORM models from JSON schema
  - `validate`: Validate JSON schema structure
  - `list-formats`: Show supported ORM formats
  - `version`: Display utility version
- Support for complex database relationships:
  - One-to-many relationships
  - Many-to-one relationships
  - Self-referencing relationships (hierarchical structures)
- Field type mapping for all supported ORM formats
- Support for primary keys, unique constraints, and default values
- Comprehensive logging system
- Template-based generation using Jinja2
- Two example schemas:
  - Blog system schema (users, posts, comments)
  - E-commerce schema (categories, products, orders, order items)

### Features
- **Prisma Generator**:
  - Full Prisma schema generation
  - Automatic relationship detection
  - Support for all Prisma data types
  - Client and datasource configuration
  - Unique constraints and default values

- **Django Generator**:
  - Django ORM model generation
  - Meta class configuration
  - Smart `__str__` method generation
  - ForeignKey, ManyToManyField, and OneToOneField support
  - Field parameters (max_length, unique, null, default, help_text)

- **SQLAlchemy Generator**:
  - SQLAlchemy declarative model generation
  - Relationship mapping
  - ForeignKey and relationship support
  - Column configuration with constraints

### Technical Details
- Built with Python 3.8+
- Uses Typer for CLI interface
- Jinja2 templating engine
- JSON Schema validation
- Rich console output
- Comprehensive test suite (84 tests)

### Installation
```bash
pip install json-to-orm
```

### Quick Start
```bash
# Generate Prisma models
json-to-orm generate schema.json output/ --format prisma

# Generate Django models
json-to-orm generate schema.json output/ --format django

# Generate SQLAlchemy models
json-to-orm generate schema.json output/ --format sqlalchemy

# Validate schema
json-to-orm validate schema.json
```

### Examples
- `examples/sample_schema.json` - Blog system schema
- `examples/ecommerce_schema.json` - E-commerce system schema

### Documentation
- Full documentation available in README.md
- Example schemas and usage patterns
- Supported field types and relationships
- CLI command reference 