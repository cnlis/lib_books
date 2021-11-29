from django.contrib import admin
from django.urls import path

from . import views

app_name = 'books'

urlpatterns = [
    path('', views.books_index, name='index'),
]
