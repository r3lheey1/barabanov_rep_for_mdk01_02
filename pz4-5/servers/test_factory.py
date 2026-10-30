# servers/test_factory.py
"""Тест: Factory создаёт разные типы изменений схемы."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django
django.setup()

from servers.models import ChangeFactory

print("=" * 60)
print("ТЕСТ FACTORY — ChangeFactory")
print("=" * 60)

print("\n1. Создаём изменения разных типов:")

alter = ChangeFactory.create("alter", "users", column="email", dtype="VARCHAR(255)")
print(f"\n✓ {alter}")
print(f"   SQL: {alter.to_sql()}")

create = ChangeFactory.create("create", "audit_log",
                              columns=["id INT", "action TEXT", "ts TIMESTAMP"])
print(f"\n✓ {create}")
print(f"   SQL: {create.to_sql()}")

drop = ChangeFactory.create("drop", "temp_table", cascade=True)
print(f"\n✓ {drop}")
print(f"   SQL: {drop.to_sql()}")

rename = ChangeFactory.create("rename", "old_users", new_name="users")
print(f"\n✓ {rename}")
print(f"   SQL: {rename.to_sql()}")

print("\n2. Доступные типы:")
print(f"   {ChangeFactory.get_available_types()}")

print("\n3. Проверяем, что все объекты — SchemaChange:")
from servers.models import SchemaChange
print(f"   all isinstance SchemaChange: "
      f"{all(isinstance(c, SchemaChange) for c in (alter, create, drop, rename))}")

print("\n4. Проверяем обработку ошибок:")
try:
    ChangeFactory.create("truncate", "users")
except ValueError as e:
    print(f"   Ошибка перехвачена: {e}")

print("\n5. Вывод:")
print("Factory создаёт объекты разных типов")
print("Клиентский код не знает о конкретных классах")
print("Обработка ошибок работает")