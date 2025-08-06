# SchemaBloom (JSON-to-ORM)

CLI-утилита для генерации ORM моделей из JSON-схем. Поддерживает Prisma, Django и SQLAlchemy.

## 🚀 Быстрый старт

```bash
# Установка
pip install json-to-orm

# Использование
json-to-orm generate schema.json models/ --format prisma

# Примеры
json-to-orm generate examples/sample_schema.json output/ --format prisma
json-to-orm validate examples/sample_schema.json
json-to-orm list-formats
```

## 🔗 Ссылки

- **Репозиторий**: https://github.com/11123aa/SchemaBloom.git

## 📋 Статус проекта

- **Статус**: В разработке
- **Прогресс**: 50% (25/50 задач выполнено)
- **Текущий этап**: Реализация генераторов моделей

## 🛠 Технологии

- Python 3.8+
- Click/Typer для CLI
- Jinja2 для шаблонов
- jsonschema для валидации 