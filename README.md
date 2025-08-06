# SchemaBloom (JSON-to-ORM)

CLI-утилита для генерации ORM моделей из JSON-схем. Поддерживает Prisma, Django и SQLAlchemy.

## 🚀 Быстрый старт

```bash
# Установка
pip install json-to-orm

# Использование
json-to-orm generate schema.json models/ --format prisma
json-to-orm generate schema.json models/ --format django
json-to-orm generate schema.json models/ --format sqlalchemy

# Примеры
json-to-orm generate examples/sample_schema.json output/ --format prisma
json-to-orm generate examples/sample_schema.json output/ --format django
json-to-orm validate examples/sample_schema.json
json-to-orm list-formats
```

## 🛠 Поддерживаемые ORM

### Prisma
- Полная поддержка всех типов данных Prisma
- Автоматическая генерация связей (one-to-many, many-to-one, many-to-many)
- Поддержка первичных ключей, уникальных полей и значений по умолчанию
- Генерация полной Prisma схемы с настройками клиента и источника данных

### Django
- Поддержка всех типов полей Django ORM (CharField, IntegerField, TextField, etc.)
- Автоматическая генерация связей (ForeignKey, ManyToManyField, OneToOneField)
- Поддержка метаданных моделей (Meta класс)
- Умная генерация метода `__str__` для моделей
- Поддержка параметров полей (max_length, unique, null, default, help_text)

### SQLAlchemy
- Поддержка в разработке
- Планируется полная поддержка всех типов SQLAlchemy

## 📋 Статус проекта

- **Статус**: В разработке
- **Прогресс**: 55% (27/50 задач выполнено)
- **Текущий этап**: Реализация генераторов моделей

### Выполненные компоненты
- ✅ Базовая инфраструктура проекта
- ✅ CLI интерфейс с полным набором команд
- ✅ JSON парсер и валидатор
- ✅ Базовый генератор моделей
- ✅ Генератор Prisma моделей
- ✅ Генератор Django моделей
- ✅ Система шаблонов Jinja2
- ✅ Система логирования

## 🔗 Ссылки

- **Репозиторий**: https://github.com/11123aa/SchemaBloom.git

## 🛠 Технологии

- Python 3.8+
- Click/Typer для CLI
- Jinja2 для шаблонов
- jsonschema для валидации 