from unicodedata import name
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entryPage, name="wikiPage"),
    path("search", views.search, name="search"),
    path("NewEntry", views.new, name="new"),
    path("random", views.random, name="random"),
    path("wiki/<str:title>/edit", views.edit, name="edit")
]
