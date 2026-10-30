# servers/singleton.py
"""Singleton: единый журнал изменений схемы БД."""

from datetime import datetime


class SchemaChangeLogger:
    """Singleton-логгер всех изменений схемы БД.

    Гарантирует, что в системе существует ровно один экземпляр,
    а значит — единая история изменений.
    """

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.changes = []      # история изменений
            cls._instance._counter = 0      # сквозной номер записи
        return cls._instance

    # ---------- публичный API ----------
    def log(self, change) -> int:
        """Записать изменение в журнал. Возвращает номер записи."""
        self._counter += 1
        self.changes.append({
            "id": self._counter,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": change.change_type,
            "description": change.get_description(),
            "sql": change.to_sql(),
        })
        return self._counter

    def get_all(self) -> list[dict]:
        return list(self.changes)

    def get_by_type(self, change_type: str) -> list[dict]:
        return [c for c in self.changes if c["type"] == change_type]

    def clear(self) -> None:
        """Сброс журнала (удобно для тестов)."""
        self.changes.clear()
        self._counter = 0