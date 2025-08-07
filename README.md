# SchemaBloom (JSON-to-ORM) 🚀

> **Transform your JSON schemas into production-ready ORM models with ease!**

A powerful CLI utility for generating ORM models from JSON schemas. Supports **Prisma**, **Django**, and **SQLAlchemy** with automatic relationship generation.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/Tests-83%20passing-brightgreen.svg)](tests/)
[![Status](https://img.shields.io/badge/Status-Production%20Ready-success.svg)](README.md#project-status)

## 🌟 Key Features

- **🔧 Multi-ORM Support**: Generate models for Prisma, Django, and SQLAlchemy
- **🔗 Automatic Relationships**: Smart detection of one-to-many, many-to-one, and many-to-many relationships
- **✅ Schema Validation**: Built-in JSON schema validation with detailed error reporting
- **🎨 Rich CLI Interface**: Beautiful terminal output with progress indicators
- **📝 Template System**: Flexible Jinja2-based template system for custom generation
- **🧪 Comprehensive Testing**: 83 unit tests covering all functionality
- **⚡ Fast & Efficient**: Optimized for performance and reliability
- **🔄 Watch Mode**: Auto-regenerate models when schema changes
- **📊 Extended Data Types**: Support for UUID, JSON, Arrays, Enums, and more
- **🔍 Interactive Mode**: Step-by-step schema creation (coming soon)
- **📤 Export/Import**: Convert between different schema formats (coming soon)

## 🚀 Quick Start

```bash
# Installation from source (recommended)
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

## 🛠 Supported ORMs

### Prisma
- Full Prisma schema generation with client and datasource configuration
- Automatic relationship mapping with `@relation` directives
- Support for all Prisma data types and field attributes
- Production-ready schema files

### Django
- Complete Django ORM model generation
- Automatic ForeignKey, ManyToManyField, and OneToOneField creation
- Smart `__str__` method generation and Meta class support
- Field parameter support (max_length, unique, null, default, help_text)

### SQLAlchemy
- Declarative model generation with declarative_base
- Automatic relationship and ForeignKey mapping
- Support for all SQLAlchemy data types and constraints
- Professional model structure

## 📋 Project Status

- **✅ Status**: Production Ready - All core functionality implemented
- **📊 Progress**: 100% Complete (50/50 tasks completed)
- **🧪 Tests**: 83/83 passing with comprehensive coverage
- **📚 Documentation**: Complete and professional
- **🔧 Architecture**: Clean, modular, and well-organized
- **📦 Package**: Built and ready for distribution
- **⚠️ Note**: PyPI experiencing network issues, use local installation or GitHub releases

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

## 🔗 Links & Resources

- **📦 Repository**: https://github.com/11123aa/SchemaBloom
- **🐍 PyPI**: https://pypi.org/project/json-to-orm/ (coming soon)
- **📖 Documentation**: https://github.com/11123aa/SchemaBloom/blob/main/README.md
- **🐛 Issues**: https://github.com/11123aa/SchemaBloom/issues
- **💡 Discussions**: https://github.com/11123aa/SchemaBloom/discussions

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

## 📖 Usage Examples

### Basic Usage
```bash
# Generate models
python -m json_to_orm generate schema.json output/ --format prisma

# Validate schema with detailed feedback
python -m json_to_orm validate-schema schema.json --verbose

# Watch for schema changes and auto-regenerate
python -m json_to_orm watch schema.json output/ --format prisma

# List all supported formats
python -m json_to_orm list-formats

# Interactive schema creation (coming soon)
python -m json_to_orm interactive
```

### Advanced Usage
```bash
# Verbose output
python -m json_to_orm generate schema.json output/ --format django --verbose

# Check version
python -m json_to_orm version
```

### Example JSON Schema
```json
{
  "name": "Blog Database",
  "description": "Simple blog database schema",
  "metadata": {
    "version": "1.0.0",
    "author": "SchemaBloom",
    "tags": ["blog", "content", "users"]
  },
  "tables": [
    {
      "name": "users",
      "description": "User accounts",
      "fields": [
        {"name": "id", "type": "uuid", "is_primary_key": true, "default_value": "gen_random_uuid()"},
        {"name": "email", "type": "email", "is_unique": true, "max_length": 255},
        {"name": "username", "type": "string", "is_unique": true, "max_length": 50},
        {"name": "password_hash", "type": "string", "max_length": 255},
        {"name": "is_active", "type": "boolean", "default_value": true},
        {"name": "created_at", "type": "datetime", "default_value": "now()"},
        {"name": "profile_data", "type": "json", "is_nullable": true}
      ],
      "indexes": [
        {"name": "idx_users_email", "fields": ["email"], "type": "btree"},
        {"name": "idx_users_username", "fields": ["username"], "type": "btree"}
      ]
    },
    {
      "name": "posts",
      "description": "Blog posts",
      "fields": [
        {"name": "id", "type": "uuid", "is_primary_key": true, "default_value": "gen_random_uuid()"},
        {"name": "title", "type": "string", "max_length": 200},
        {"name": "content", "type": "text"},
        {"name": "status", "type": "enum", "enum_values": ["draft", "published", "archived"], "default_value": "draft"},
        {"name": "author_id", "type": "uuid"},
        {"name": "created_at", "type": "datetime", "default_value": "now()"},
        {"name": "updated_at", "type": "datetime", "default_value": "now()"}
      ]
    }
  ],
  "relationships": [
    {
      "name": "UserPosts",
      "type": "one_to_many",
      "from": "users",
      "to": "posts",
      "foreign_key": "author_id",
      "referenced_key": "id",
      "on_delete": "cascade",
      "on_update": "cascade"
    }
  ]
}
```

## 🛠 Technologies & Dependencies

- **🐍 Python 3.8+**: Full compatibility with modern Python versions
- **⚡ Typer**: Modern CLI framework with automatic help generation
- **🎨 Jinja2**: Powerful template engine for flexible code generation
- **✅ jsonschema**: Robust JSON schema validation
- **🎯 Rich**: Beautiful terminal output and progress indicators
- **🔧 Pydantic**: Data validation and settings management

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

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with modern Python best practices
- Inspired by the need for efficient ORM model generation
- Community-driven development approach

---

**SchemaBloom** - Transform your JSON schemas into production-ready ORM models with ease! 🚀

*Keywords: JSON to ORM, Prisma generator, Django models, SQLAlchemy models, code generation, database models, schema converter, ORM tools, Python CLI, JSON schema validation*