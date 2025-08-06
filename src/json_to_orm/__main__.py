"""
Точка входа для запуска CLI утилиты.

Этот модуль позволяет запускать CLI утилиту командой:
python -m json_to_orm
"""

from .cli import app

if __name__ == "__main__":
    app()
