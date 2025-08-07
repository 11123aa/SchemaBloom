# SchemaBloom (JSON-to-ORM)

A powerful CLI utility for generating ORM models from JSON schemas. Supports Prisma, Django, and SQLAlchemy.

## 🚀 Quick Start

```bash
# Installation from source (recommended)
git clone https://github.com/11123aa/SchemaBloom.git
cd SchemaBloom
pip install -e .

# Usage
python -m json_to_orm generate schema.json models/ --format prisma
python -m json_to_orm generate schema.json models/ --format django
python -m json_to_orm generate schema.json models/ --format sqlalchemy

# Examples
python -m json_to_orm generate examples/sample_schema.json output/ --format prisma
python -m json_to_orm generate examples/sample_schema.json output/ --format django
python -m json_to_orm generate examples/ecommerce_schema.json output/ --format sqlalchemy
python -m json_to_orm validate examples/sample_schema.json
python -m json_to_orm list-formats
```

## 🛠 Supported ORMs

### Prisma
- Full support for all Prisma data types
- Automatic relationship generation (one-to-many, many-to-one, many-to-many)
- Support for primary keys, unique fields, and default values
- Complete Prisma schema generation with client and datasource configuration

### Django
- Support for all Django ORM field types (CharField, IntegerField, TextField, etc.)
- Automatic relationship generation (ForeignKey, ManyToManyField, OneToOneField)
- Model metadata support (Meta class)
- Smart `__str__` method generation for models
- Field parameter support (max_length, unique, null, default, help_text)

### SQLAlchemy
- Full support for all SQLAlchemy data types
- Automatic relationship generation (relationship)
- Support for primary keys, unique fields, and default values
- Model generation using declarative_base
- ForeignKey and relationship support

## 📋 Project Status

- **Status**: Ready for use, package prepared for PyPI publication
- **Progress**: 100% (50/50 tasks completed)
- **Current Stage**: Project fully completed
- **Last Commit**: Final cleanup and documentation
- **Version**: 1.0.0 (locally built)

### Completed Components
- ✅ JSON parser and validator
- ✅ Base model generator
- ✅ Prisma model generator (with relationship support)
- ✅ Django model generator (with relationship support)
- ✅ SQLAlchemy model generator (with relationship support)
- ✅ Jinja2 template system
- ✅ Logging system
- ✅ Primary key and unique field handling
- ✅ Default value support
- ✅ Automatic table relationship generation
- ✅ Git integration and versioning
- ✅ **Complete unit test suite (83 tests)**
- ✅ **Integration tests**
- ✅ **Error handling and edge case tests**

## 🔗 Links

- **Repository**: https://github.com/11123aa/SchemaBloom.git
- **PyPI**: https://pypi.org/project/json-to-orm/ (when published)

## 📦 Installation

### Installation from source (recommended)
```bash
# Clone repository
git clone https://github.com/11123aa/SchemaBloom.git
cd SchemaBloom

# Install in development mode
pip install -e .

# Usage
python -m json_to_orm --help
```

### Installation from built files
```bash
# Download files from repository (dist/ folder)
# Install from local files
pip install json_to_orm-1.0.0-py3-none-any.whl
```

### Installation from PyPI (when available)
```bash
# Install from PyPI (after publication)
pip install json-to-orm
```

**Note**: Currently, the package is ready for PyPI publication but has network connection issues. Installation from source is recommended.

## 🛠 Technologies

- Python 3.8+ (full compatibility with Python 3.9+)
- Click/Typer for CLI
- Jinja2 for templates
- jsonschema for validation
- Pydantic for data validation
- Rich for beautiful terminal output

## 📖 Usage Examples

### Validate schema
```bash
python -m json_to_orm validate examples/sample_schema.json
```

### Generate Prisma models
```bash
python -m json_to_orm generate examples/sample_schema.json output/ --format prisma
```

### Generate Django models
```bash
python -m json_to_orm generate examples/sample_schema.json output/ --format django
```

### Generate SQLAlchemy models
```bash
python -m json_to_orm generate examples/sample_schema.json output/ --format sqlalchemy
```

### List available formats
```bash
python -m json_to_orm list-formats
```

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.