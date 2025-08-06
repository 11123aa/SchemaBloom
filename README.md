# JSON-to-ORM

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Development Status](https://img.shields.io/badge/status-alpha-orange.svg)](https://github.com/json-to-orm/json-to-orm)

CLI-утилита для автоматической генерации ORM моделей из JSON-схем данных. Поддерживает генерацию моделей для популярных ORM фреймворков: Prisma, Django и SQLAlchemy.

## 🚀 Возможности

- **Множественные ORM**: Поддержка Prisma, Django и SQLAlchemy
- **Простой CLI**: Интуитивно понятный интерфейс командной строки
- **Валидация схем**: Проверка корректности JSON-схем
- **Расширяемость**: Легкое добавление новых ORM фреймворков
- **Красивый вывод**: Цветной и структурированный вывод с помощью Rich

## 📋 Требования

- Python 3.8 или выше
- pip (менеджер пакетов Python)

## 🛠️ Установка

### Из исходного кода

```bash
# Клонирование репозитория
git clone https://github.com/json-to-orm/json-to-orm.git
cd json-to-orm

# Создание виртуального окружения
python -m venv venv
source venv/bin/activate  # На Linux/macOS
# или
venv\Scripts\activate     # На Windows

# Установка зависимостей
pip install -e .
```

### Разработка

```bash
# Установка зависимостей для разработки
pip install -e ".[dev]"

# Настройка pre-commit hooks
pre-commit install
```

## 📖 Использование

### Основные команды

```bash
# Генерация моделей
json-to-orm generate schema.json models/ --format prisma

# Валидация схемы
json-to-orm validate schema.json

# Список поддерживаемых форматов
json-to-orm list-formats

# Версия утилиты
json-to-orm version
```

### Примеры использования

#### Генерация Prisma схемы

```bash
json-to-orm generate schema.json models/ --format prisma --verbose
```

#### Генерация Django моделей

```bash
json-to-orm generate schema.json models/ --format django
```

#### Генерация SQLAlchemy моделей

```bash
json-to-orm generate schema.json models/ --format sqlalchemy
```

#### Валидация схемы с подробным выводом

```bash
json-to-orm validate schema.json --verbose
```

## 📝 Формат JSON-схемы

### Пример схемы

```json
{
  "tables": [
    {
      "name": "users",
      "fields": [
        {
          "name": "id",
          "type": "integer",
          "primary_key": true,
          "auto_increment": true
        },
        {
          "name": "email",
          "type": "string",
          "unique": true,
          "nullable": false
        },
        {
          "name": "created_at",
          "type": "datetime",
          "default": "now()"
        }
      ]
    },
    {
      "name": "posts",
      "fields": [
        {
          "name": "id",
          "type": "integer",
          "primary_key": true,
          "auto_increment": true
        },
        {
          "name": "title",
          "type": "string",
          "nullable": false
        },
        {
          "name": "user_id",
          "type": "integer",
          "nullable": false
        }
      ]
    }
  ],
  "relationships": [
    {
      "from": "users",
      "to": "posts",
      "type": "one_to_many",
      "foreign_key": "user_id"
    }
  ]
}
```

### Поддерживаемые типы данных

- `string` - строковый тип
- `integer` - целочисленный тип
- `float` - тип с плавающей точкой
- `boolean` - логический тип
- `datetime` - тип даты и времени
- `json` - JSON тип
- `array` - массив
- `enum` - перечисление

## 🏗️ Архитектура

```
json-to-orm/
├── src/json_to_orm/
│   ├── cli.py              # CLI интерфейс
│   ├── core.py             # Основной класс JSONToORM
│   ├── parser/             # Парсинг и валидация JSON
│   ├── generators/         # Генераторы моделей
│   ├── templates/          # Шаблоны для генерации
│   └── utils/              # Вспомогательные функции
├── tests/                  # Тесты
├── examples/               # Примеры использования
└── docs/                   # Документация
```

## 🧪 Тестирование

```bash
# Запуск всех тестов
pytest

# Запуск тестов с покрытием
pytest --cov=src

# Запуск тестов с подробным выводом
pytest -v
```

## 📚 Документация

Подробная документация доступна в папке [docs/](docs/):

- [Project.md](docs/Project.md) - Детальное описание проекта
- [Tasktracker.md](docs/Tasktracker.md) - Отслеживание задач
- [Diary.md](docs/Diary.md) - Дневник разработки
- [qa.md](docs/qa.md) - Вопросы по архитектуре

## 🤝 Вклад в проект

Мы приветствуем вклад в развитие проекта! Пожалуйста, ознакомьтесь с нашими [правилами контрибьюции](CONTRIBUTING.md).

### Процесс разработки

1. Форкните репозиторий
2. Создайте ветку для новой функции (`git checkout -b feature/amazing-feature`)
3. Внесите изменения и зафиксируйте их (`git commit -m 'Add amazing feature'`)
4. Отправьте изменения в ветку (`git push origin feature/amazing-feature`)
5. Откройте Pull Request

## 📄 Лицензия

Этот проект распространяется под лицензией MIT. См. файл [LICENSE](LICENSE) для получения дополнительной информации.

## 🐛 Сообщения об ошибках

Если вы нашли ошибку, пожалуйста, создайте issue в [GitHub Issues](https://github.com/json-to-orm/json-to-orm/issues).

## 📞 Поддержка

Если у вас есть вопросы или нужна помощь, пожалуйста:

- Создайте issue в GitHub
- Обратитесь к документации в папке [docs/](docs/)
- Проверьте [FAQ](docs/FAQ.md)

## 🗺️ Планы развития

### Краткосрочные планы (3-6 месяцев)
- [ ] Поддержка дополнительных ORM фреймворков
- [ ] Улучшение валидации схем
- [ ] Добавление интерактивного режима
- [ ] Интеграция с IDE

### Долгосрочные планы (6-12 месяцев)
- [ ] Веб-интерфейс для генерации
- [ ] Поддержка миграций
- [ ] Интеграция с системами контроля версий
- [ ] Плагинная архитектура

---

**JSON-to-ORM** - ускоряем разработку с автоматической генерацией ORM моделей! 🚀 