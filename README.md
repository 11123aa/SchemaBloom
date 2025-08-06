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
- Полная поддержка всех типов данных SQLAlchemy
- Автоматическая генерация связей (relationship)
- Поддержка первичных ключей, уникальных полей и значений по умолчанию
- Генерация моделей с использованием declarative_base
- Поддержка ForeignKey и relationship связей

## 📋 Статус проекта

- **Статус**: Готов к релизу
- **Прогресс**: 100% (50/50 задач выполнено)
- **Текущий этап**: Проект завершен
- **Последний коммит**: Git инициализация и финальное тестирование

### Выполненные компоненты
- ✅ JSON парсер и валидатор
- ✅ Базовый генератор моделей
- ✅ Генератор Prisma моделей (с поддержкой связей)
- ✅ Генератор Django моделей (с поддержкой связей)
- ✅ Генератор SQLAlchemy моделей (с поддержкой связей)
- ✅ Система шаблонов Jinja2
- ✅ Система логирования
- ✅ Обработка первичных ключей и уникальных полей
- ✅ Поддержка значений по умолчанию
- ✅ Автоматическая генерация связей между таблицами
- ✅ Git интеграция и версионирование
- ✅ **Полный набор unit-тестов (84 теста)**
- ✅ **Интеграционные тесты**
- ✅ **Тесты обработки ошибок и граничных случаев**

## 🔗 Ссылки

- **Репозиторий**: https://github.com/11123aa/SchemaBloom.git

## 🛠 Технологии

- Python 3.8+
- Click/Typer для CLI
- Jinja2 для шаблонов
- jsonschema для валидации 