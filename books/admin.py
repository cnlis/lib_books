from django.contrib import admin

from .models import Book, Grade, Language, Publisher, Source, Special

class BookAdmin(admin.ModelAdmin):
    list_display = ('code', 'author', 'title', 'grades', 'publisher', 'language', 'special')


admin.site.register(Source)
admin.site.register(Grade)
admin.site.register(Publisher)
admin.site.register(Language)
admin.site.register(Special)
admin.site.register(Book, BookAdmin)
