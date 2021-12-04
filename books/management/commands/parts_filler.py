import re

from django.core.management.base import BaseCommand

from books.models import Book


class Command(BaseCommand):
    def handle(self, *args, **options):
        books = Book.objects.all()
        for book in books:
            result = re.findall(r'в \d{1}\ час', book.title)
            if result:
                book.parts = int(result[0].split()[1])
                book.save()
