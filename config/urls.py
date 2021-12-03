from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path('books/', include('books.urls', namespace='books')),
    path('', include('funds.urls', namespace='funds')),
    path('admin/', admin.site.urls),
]
