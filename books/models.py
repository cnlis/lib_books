import re

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models, IntegrityError, transaction
from django.db.models.constraints import UniqueConstraint


def crop_text(s):
    if len(s) <= 40:
        return s
    return s[:40]+'...'


class Category(models.Model):
    code = models.CharField(max_length=17, unique=True)
    title = models.CharField(max_length=300)

    def __str__(self):
        return f'{self.code}\t{self.title[:80]}'

    def clean_fields(self, exclude=('title',)):
        s = self.code.replace('.', '')
        if not s.isnumeric():
            raise ValidationError('Код категории не соответствует формату!')


class Grade(models.Model):
    title = models.CharField(max_length=15, default='1', unique=True)

    def __str__(self):
        return self.title

    @staticmethod
    def parse_title(string):
        grade_parse = re.findall(r'\d{1,2}', str(string))
        suffix_parse = re.findall(r'[A-я.]+', str(string))
        grade_from = int(grade_parse[0])
        grade_to = int(grade_parse[1]) if len(grade_parse) == 2 else grade_from
        suffix = suffix_parse[0] if suffix_parse else ''
        if grade_from == grade_to:
            return f'{grade_from}{suffix}'
        else:
            return f'{grade_from} - {grade_to}{suffix}'


class Publisher(models.Model):
    title = models.TextField(max_length=200, unique=True, default='неизвестно')

    def __str__(self):
        return self.title


class Language(models.Model):
    title = models.TextField(max_length=50, unique=True, default='русский язык')

    def __str__(self):
        return self.title


class Special(models.Model):
    title = models.TextField(max_length=50, unique=True, default='-')

    def __str__(self):
        return self.title


class Source(models.Model):
    title = models.TextField(max_length=20, default='неизвестно')
    date = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            UniqueConstraint(fields=['title', 'date'], name='unique_source'),
        ]

    def __str__(self):
        return self.title


class System(models.Model):
    title = models.CharField(max_length=200, default='нет', unique=True)

    def __str__(self):
        return self.title


def blank_class():
    return Grade.objects.get_or_create(id=1)[0].id


def blank_publisher():
    return Publisher.objects.get_or_create(id=1)[0].id


def blank_language():
    return Language.objects.get_or_create(id=1)[0].id


def blank_source():
    return Source.objects.get_or_create(id=1)[0].id


def blank_special():
    return Special.objects.get_or_create(id=1)[0].id


def blank_system():
    return System.objects.get_or_create(id=1)[0].id


class Book(models.Model):
    source = models.ForeignKey(
        Source,
        on_delete=models.SET_DEFAULT,
        default=blank_source,
        related_name='books',
    )
    system = models.ForeignKey(
        System,
        on_delete=models.SET_DEFAULT,
        default=blank_system,
        related_name='books',
    )
    code = models.CharField(max_length=17)
    author = models.TextField(max_length=300)
    title = models.TextField(max_length=300)
    parts = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    grades = models.ForeignKey(
        Grade,
        on_delete=models.SET_DEFAULT,
        default=blank_class,
        related_name='books',
    )
    publisher = models.ForeignKey(
        Publisher,
        on_delete=models.SET_DEFAULT,
        default=blank_publisher,
        related_name='books',
    )
    language = models.ForeignKey(
        Language,
        on_delete=models.SET_DEFAULT,
        default=blank_language,
        related_name='books',
    )
    special = models.ForeignKey(
        Special,
        on_delete=models.SET_DEFAULT,
        default=blank_special,
        related_name='books',
    )

    def __str__(self):
        return f'{crop_text(self.author)} - {crop_text(self.title)} - {self.grades} кл. (ОС: {self.system}) ({self.source})'

    def clean_fields(self, exclude=('id', 'source', 'author', 'title',
                                    'grades', 'publisher', 'language',
                                    'special', 'system')):
        s = self.code.replace('.', '')
        if not s.isnumeric():
            raise ValidationError('Код книги не соответствует формату!')
