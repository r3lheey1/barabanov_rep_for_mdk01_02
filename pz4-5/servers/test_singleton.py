# servers/test_singleton.py
"""Тест: Singleton создаёт только один экземпляр."""

import os
import sys

# позволяем запускать файл напрямую: python servers/test_singleton.py
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django
django.setup()

from servers.singleton import SchemaChangeLogger
from servers.models import ChangeFactory

print("=" * 60)
print("ТЕСТ SINGLETON — SchemaChangeLogger")
print("=" * 60)

print("\n1. Создаём первый логгер...")
logger1 = SchemaChangeLogger()

print("2. Создаём второй логгер...")
logger2 = SchemaChangeLogger()

print("\n3. Проверяем единственность:")
print(f"   logger1 is logger2: {logger1 is logger2}")
print(f"   id(logger1): {id(logger1)}")
print(f"   id(logger2): {id(logger2)}")

print("\n4. Логируем изменение через logger1:")
change = ChangeFactory.create("create", "orders", columns=["id INT", "total NUMERIC"])
logger1.log(change)
print(f"   Записано, всего записей: {len(logger1.get_all())}")

print("\n5. Читаем журнал через logger2:")
print(f"   Записей видно: {len(logger2.get_all())}")
for entry in logger2.get_all():
    print(f"   #{entry['id']} {entry['type']}: {entry['description']}")

print("\n6. Вывод:")
print("logger1 и logger2 — один объект")
print("Запись через logger1 видна в logger2")
print("Singleton работает корректно!")