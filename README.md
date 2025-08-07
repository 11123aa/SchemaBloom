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
json-to-orm generate examples/ecommerce_schema.json output/ --format sqlalchemy
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

- **Статус**: Проект готов, требуется ручная публикация на PyPI
- **Прогресс**: 98% (49/50 задач выполнено)
- **Текущий этап**: Пакет готов к публикации
- **Последний коммит**: Проблема с автоматической публикацией на PyPI
- **Версия**: 1.0.0 (локально собрана)

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
- ✅ **Полный набор unit-тестов (83 теста)**
- ✅ **Интеграционные тесты**
- ✅ **Тесты обработки ошибок и граничных случаев**

## 🔗 Ссылки

- **Репозиторий**: https://github.com/11123aa/SchemaBloom.git
- **PyPI**: https://pypi.org/project/json-to-orm/

## 📦 Установка

```bash
# Установка из PyPI
pip install json-to-orm

# Установка из исходного кода
git clone https://github.com/11123aa/SchemaBloom.git
cd SchemaBloom
pip install -e .
```

## 🛠 Технологии

- Python 3.8+ (полная совместимость с Python 3.9+)
- Click/Typer для CLI
- Jinja2 для шаблонов
- jsonschema для валидации
- Pydantic для валидации данных
- Rich для красивого вывода в терминале

## 📖 Примеры использования

### Валидация схемы
```bash
json-to-orm validate examples/sample_schema.json
```

### Генерация Prisma моделей
```bash
json-to-orm generate examples/sample_schema.json output/ --format prisma
```

### Генерация Django моделей
```bash
json-to-orm generate examples/sample_schema.json output/ --format django
```

### Генерация SQLAlchemy моделей
```bash
json-to-orm generate examples/sample_schema.json output/ --format sqlalchemy
```

### Просмотр доступных форматов
```bash
json-to-orm list-formats
```

## 📄 Лицензия

MIT License - см. файл [LICENSE](LICENSE) для подробностей.