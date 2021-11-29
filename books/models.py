import re

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.constraints import UniqueConstraint


class Categorie(models.Model):
    code = models.CharField(max_length=17, unique=True)
    title = models.CharField(max_length=300)

    def __str__(self):
        return f'{self.code} {self.title[:40]}'

    def clean_fields(self, exclude=('title',)):
        s = self.code.replace('.', '')
        if not s.isnumeric():
            raise ValidationError('Код категории не соответствует формату!')


class Klass(models.Model):
    class_from = models.IntegerField(default=1)
    class_to = models.IntegerField(default=1)
    suffix = models.CharField(max_length=5, blank=True)

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['class_from', 'class_to', 'suffix'],
                name='unique_class'
            ),
        ]

    def clean_fields(self, exclude=('suffix',)):
        if (self.class_from < 1) or (self.class_from > 11):
            raise ValidationError('Класс должен быть от 1 до 11!')
        if self.class_to <= self.class_from:
            self.class_to = self.class_from

    def __str__(self):
        if self.class_from == self.class_to:
            return f'{self.class_from}{self.suffix}'
        return f'{self.class_from} - {self.class_to}{self.suffix}'

    @staticmethod
    def parse_string(string):
        class_parse = re.findall(r'\d{1,2}', string)
        suffix_parse = re.findall(r'[A-я.]+', string)
        class_from = int(class_parse[0])
        class_to = int(class_parse[1]) if len(class_parse) == 2 else class_from
        suffix = suffix_parse[0] if suffix_parse else ''
        return class_from, class_to, suffix


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


def blank_class():
    return Klass.objects.get_or_create(id=1)[0].id


def blank_publisher():
    return Publisher.objects.get_or_create(id=1)[0].id


def blank_language():
    return Language.objects.get_or_create(id=1)[0].id


def blank_source():
    return Source.objects.get_or_create(id=1)[0].id


def blank_special():
    return Special.objects.get_or_create(id=1)[0].id


class Book(models.Model):
    source = models.ForeignKey(
        Source,
        on_delete=models.SET_DEFAULT,
        default=blank_source,
        related_name='books',
    )
    code = models.CharField(max_length=17)
    author = models.TextField(max_length=300)
    title = models.TextField(max_length=300)
    classes = models.ForeignKey(
        Klass,
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

    def clean_fields(self, exclude=('id', 'source', 'author', 'title',
                                    'classes', 'publisher', 'language',
                                    'special')):
        s = self.code.replace('.', '')
        if not s.isnumeric():
            raise ValidationError('Код книги не соответствует формату!')
