# servers/models.py
"""Factory: создание объектов изменений схемы БД."""


# ---------- Базовый класс ----------
class SchemaChange:
    """Базовое изменение схемы БД."""

    change_type: str = "UNKNOWN"

    def __init__(self, table: str, **kwargs):
        self.table = table
        self.params = kwargs

    def get_description(self) -> str:
        raise NotImplementedError()

    def to_sql(self) -> str:
        raise NotImplementedError()

    def __str__(self) -> str:
        return f"[{self.change_type}] {self.get_description()}"


# ---------- Наследники ----------
class AlterChange(SchemaChange):
    """ALTER TABLE — изменение структуры таблицы."""

    change_type = "ALTER"

    def get_description(self) -> str:
        column = self.params.get("column", "?")
        action = self.params.get("action", "MODIFY")
        return f"Изменение колонки '{column}' ({action}) в таблице '{self.table}'"

    def to_sql(self) -> str:
        column = self.params.get("column", "?")
        dtype = self.params.get("dtype", "TEXT")
        return f"ALTER TABLE {self.table} ALTER COLUMN {column} TYPE {dtype};"


class CreateChange(SchemaChange):
    """CREATE TABLE — создание таблицы."""

    change_type = "CREATE"

    def get_description(self) -> str:
        columns = ", ".join(self.params.get("columns", [])) or "id INT"
        return f"Создание таблицы '{self.table}' ({columns})"

    def to_sql(self) -> str:
        columns = ", ".join(self.params.get("columns", [])) or "id INT"
        return f"CREATE TABLE {self.table} ({columns});"


class DropChange(SchemaChange):
    """DROP TABLE — удаление таблицы."""

    change_type = "DROP"

    def get_description(self) -> str:
        cascade = " CASCADE" if self.params.get("cascade") else ""
        return f"Удаление таблицы '{self.table}'{cascade}"

    def to_sql(self) -> str:
        cascade = " CASCADE" if self.params.get("cascade") else ""
        return f"DROP TABLE {self.table}{cascade};"


class RenameChange(SchemaChange):
    """RENAME — переименование таблицы или колонки."""

    change_type = "RENAME"

    def get_description(self) -> str:
        new_name = self.params.get("new_name", "?")
        return f"Переименование '{self.table}' → '{new_name}'"

    def to_sql(self) -> str:
        new_name = self.params.get("new_name", "?")
        return f"ALTER TABLE {self.table} RENAME TO {new_name};"


# ---------- Фабрика ----------
class ChangeFactory:
    """Фабрика изменений схемы БД."""

    _registry = {
        "alter": AlterChange,
        "create": CreateChange,
        "drop": DropChange,
        "rename": RenameChange,
    }

    @classmethod
    def create(cls, change_type: str, table: str, **kwargs) -> SchemaChange:
        key = change_type.lower()
        if key not in cls._registry:
            raise ValueError(
                f"Неизвестный тип изменения: '{change_type}'. "
                f"Доступные: {cls.get_available_types()}"
            )
        return cls._registry[key](table, **kwargs)

    @classmethod
    def get_available_types(cls) -> list[str]:
        return list(cls._registry.keys())

    @classmethod
    def register(cls, name: str, change_cls: type) -> None:
        """Расширение фабрики без правки исходного кода."""
        cls._registry[name.lower()] = change_cls