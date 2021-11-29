from django.core.management.base import BaseCommand

from books.parsers.categories_import import category_parser


class Command(BaseCommand):
    def handle(self, *args, **options):
        category_parser()
