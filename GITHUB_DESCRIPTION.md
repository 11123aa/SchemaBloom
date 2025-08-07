# SchemaBloom (JSON-to-ORM)

A powerful CLI utility for generating ORM models from JSON schemas. Supports Prisma, Django, and SQLAlchemy with automatic relationship generation.

## 🌟 Features

- **Multi-ORM Support**: Generate models for Prisma, Django, and SQLAlchemy
- **Automatic Relationships**: Smart detection and generation of one-to-many, many-to-one, and many-to-many relationships
- **Schema Validation**: Built-in JSON schema validation with detailed error reporting
- **Rich CLI Interface**: Beautiful terminal output with progress indicators
- **Template System**: Flexible Jinja2-based template system for custom generation
- **Comprehensive Testing**: 83 unit tests covering all functionality

## 🚀 Quick Start

```bash
# Clone and install
git clone https://github.com/11123aa/SchemaBloom.git
cd SchemaBloom
pip install -e .

# Generate Prisma models
python -m json_to_orm generate schema.json models/ --format prisma

# Generate Django models
python -m json_to_orm generate schema.json models/ --format django

# Generate SQLAlchemy models
python -m json_to_orm generate schema.json models/ --format sqlalchemy

# Validate schema
python -m json_to_orm validate schema.json
```

## 📋 Project Status

- ✅ **Complete**: All core functionality implemented
- ✅ **Tested**: 83 tests passing
- ✅ **Documented**: Comprehensive documentation and examples
- 🔄 **Ready for PyPI**: Package prepared for publication

## 🛠 Supported ORMs

### Prisma
- Full Prisma schema generation with client and datasource configuration
- Automatic relationship mapping with `@relation` directives
- Support for all Prisma data types and field attributes

### Django
- Complete Django ORM model generation
- Automatic ForeignKey, ManyToManyField, and OneToOneField creation
- Smart `__str__` method generation and Meta class support

### SQLAlchemy
- Declarative model generation with declarative_base
- Automatic relationship and ForeignKey mapping
- Support for all SQLAlchemy data types and constraints

## 📦 Installation

### From Source (Recommended)
```bash
git clone https://github.com/11123aa/SchemaBloom.git
cd SchemaBloom
pip install -e .
```

### From Built Files
```bash
# Download files from repository (dist/ folder)
pip install json_to_orm-1.0.0-py3-none-any.whl
```

## 📖 Usage Examples

### Basic Usage
```bash
# Generate models
python -m json_to_orm generate schema.json output/ --format prisma

# Validate schema
python -m json_to_orm validate schema.json

# List supported formats
python -m json_to_orm list-formats
```

### Advanced Usage
```bash
# Verbose output
python -m json_to_orm generate schema.json output/ --format django --verbose

# Check version
python -m json_to_orm version
```

## 🔧 Technologies

- **Python 3.8+**: Full compatibility with modern Python versions
- **Typer**: Modern CLI framework with automatic help generation
- **Jinja2**: Powerful template engine for flexible code generation
- **jsonschema**: Robust JSON schema validation
- **Rich**: Beautiful terminal output and progress indicators
- **Pydantic**: Data validation and settings management

## 📁 Project Structure

```
SchemaBloom/
├── src/json_to_orm/          # Main package
│   ├── generators/           # ORM generators (Prisma, Django, SQLAlchemy)
│   ├── parser/              # JSON parsing and validation
│   ├── utils/               # Utilities and helpers
│   └── templates/           # Jinja2 templates
├── examples/                # Example JSON schemas
├── tests/                   # Comprehensive test suite
└── docs/                    # Documentation
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🔗 Links

- **Repository**: https://github.com/11123aa/SchemaBloom
- **Issues**: https://github.com/11123aa/SchemaBloom/issues
- **Documentation**: https://github.com/11123aa/SchemaBloom/blob/main/README.md

---

**SchemaBloom** - Transform your JSON schemas into production-ready ORM models with ease! 🚀
