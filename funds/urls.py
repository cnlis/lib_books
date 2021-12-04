from django.urls import path

from . import views

app_name = 'funds'

urlpatterns = [
    path('', views.funds_index, name='index'),
    path('incomes/', views.funds_income_list, name='income_list'),
    path('incomes/<int:doc_id>/', views.funds_income_detail, name='income_detail'),
    path('incomes/<int:doc_id>/del/', views.funds_income_del, name='income_del'),
    path('incomes/<int:doc_id>/<int:record_id>/del/', views.funds_income_book_del, name='income_book_del'),
    path('incomes/<int:doc_id>/edit', views.funds_income_edit, name='income_edit'),
    path('<int:book_id>/', views.funds_book_detail, name='book_detail'),
]
