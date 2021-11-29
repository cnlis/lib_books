from django.contrib import admin

from .models import Book, Klass, Language, Publisher, Source, Special

class BookAdmin(admin.ModelAdmin):
    list_display = ('code', 'author', 'title', 'classes', 'publisher', 'language', 'special')


admin.site.register(Source)
admin.site.register(Klass)
admin.site.register(Publisher)
admin.site.register(Language)
admin.site.register(Special)
admin.site.register(Book, BookAdmin)
