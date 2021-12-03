from django.core.management.base import BaseCommand

from books.parsers.categories_import import category_parser, category_saver


class Command(BaseCommand):
    def handle(self, *args, **options):
        categories = category_parser()
        category_saver(categories)
