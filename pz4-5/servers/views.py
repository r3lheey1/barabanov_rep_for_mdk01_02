# servers/views.py
"""View для демонстрации Singleton + Factory."""

from django.http import HttpResponse, JsonResponse

from .models import ChangeFactory
from .singleton import SchemaChangeLogger


def index(request):
    """Главная: демонстрирует работу Singleton и Factory."""
    logger = SchemaChangeLogger()

    # 1. Factory создаёт изменения разных типов
    changes = [
        ChangeFactory.create("create", "users",
                             columns=["id INT", "name VARCHAR(100)"]),
        ChangeFactory.create("alter", "users",
                             column="name", dtype="VARCHAR(255)"),
        ChangeFactory.create("rename", "users", new_name="app_users"),
        ChangeFactory.create("drop", "old_logs", cascade=True),
    ]

    # 2. Singleton логирует их в единый журнал
    for change in changes:
        logger.log(change)

    # 3. Singleton доказывает единственность
    logger2 = SchemaChangeLogger()
    same = logger is logger2

    html = "<h1>Журнал изменений схемы БД</h1>"
    html += "<h2>Factory: создано объектов — {}</h2>".format(len(changes))
    html += "<ul>"
    for c in changes:
        html += f"<li><b>{c.change_type}</b>: {c.get_description()}"
        html += f"<br><code>{c.to_sql()}</code></li>"
    html += "</ul>"

    html += "<h2>Singleton: единый журнал</h2>"
    html += f"<p>logger is logger2 → <b>{same}</b></p>"
    html += "<p>Записей в журнале: <b>{}</b></p>".format(len(logger.get_all()))

    html += "<h2>Журнал</h2><table border='1' cellpadding='6'>"
    html += "<tr><th>#</th><th>Время</th><th>Тип</th><th>Описание</th><th>SQL</th></tr>"
    for e in logger.get_all():
        html += (
            f"<tr><td>{e['id']}</td><td>{e['timestamp']}</td>"
            f"<td>{e['type']}</td><td>{e['description']}</td>"
            f"<td><code>{e['sql']}</code></td></tr>"
        )
    html += "</table>"

    return HttpResponse(html)


def changes_json(request):
    """JSON-представление журнала (второй маршрут)."""
    logger = SchemaChangeLogger()
    return JsonResponse({
        "total": len(logger.get_all()),
        "available_types": ChangeFactory.get_available_types(),
        "changes": logger.get_all(),
    }, json_dumps_params={"ensure_ascii": False, "indent": 2})