# SchemaBloom v1.0.0 - Initial Release

## 🎉 SchemaBloom JSON-to-ORM CLI Utility

SchemaBloom is a powerful CLI utility that generates ORM models from JSON schemas. It supports multiple ORM formats including Prisma, Django, and SQLAlchemy.

## ✨ Key Features

### 🔧 Multi-ORM Support
- **Prisma**: Full schema generation with relationships and constraints
- **Django**: ORM models with Meta classes and smart `__str__` methods
- **SQLAlchemy**: Declarative models with relationship mapping

### 🚀 CLI Interface
- `generate`: Generate ORM models from JSON schema
- `validate`: Validate JSON schema structure
- `list-formats`: Show supported ORM formats
- `version`: Display utility version

### 🔗 Advanced Features
- Complex database relationships (one-to-many, many-to-one, self-referencing)
- Field type mapping for all supported ORM formats
- Primary keys, unique constraints, and default values
- Template-based generation using Jinja2
- Comprehensive logging system

## 📦 Installation

```bash
pip install json-to-orm
```

## 🚀 Quick Start

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

## 📚 Examples

The repository includes two comprehensive examples:

1. **Blog System Schema** (`examples/sample_schema.json`)
   - Users, Posts, Comments with relationships
   - Demonstrates basic CRUD operations

2. **E-commerce Schema** (`examples/ecommerce_schema.json`)
   - Categories, Products, Orders, Order Items
   - Shows complex hierarchical relationships

## 🛠 Technical Details

- **Python**: 3.8+
- **CLI Framework**: Typer
- **Templating**: Jinja2
- **Validation**: JSON Schema
- **Testing**: 84 comprehensive tests
- **License**: MIT

## 🔗 Links

- **Repository**: https://github.com/11123aa/SchemaBloom
- **Documentation**: See README.md for detailed usage
- **Issues**: https://github.com/11123aa/SchemaBloom/issues

## 🎯 What's Next

This is the initial release of SchemaBloom. Future versions will include:
- Support for additional ORM frameworks
- Web interface for visual schema editing
- Database migration generation
- Enhanced relationship handling

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

**SchemaBloom Team** - Making ORM model generation simple and efficient! 🚀 