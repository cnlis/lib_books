from django.core.management.base import BaseCommand

from books.parsers.books_import import books_parser, books_saver


class Command(BaseCommand):
    def handle(self, *args, **options):
        books = books_parser(144)
        books_saver(books, 'ФПУ')
