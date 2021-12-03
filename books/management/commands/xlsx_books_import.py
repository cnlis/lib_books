import os

from django.core.management.base import BaseCommand, CommandError

from books.parsers.books_import import books_saver
from books.parsers.xlsx_import_export import xlsx_read


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('file', type=str)

    def handle(self, *args, **options):
        file_path = options['file']
        # if not os.path.exists(file_path):
        #     raise CommandError(f'file {file_path} doesn\'t exists')
        books = xlsx_read(file_path, 7)
        books_saver(books, 'ФПУ')
