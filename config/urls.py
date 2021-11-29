from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path('', include('books.urls', namespace='books')),
    path('admin/', admin.site.urls),
]
