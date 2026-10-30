# servers/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("changes/", views.changes_json, name="changes_json"),
]