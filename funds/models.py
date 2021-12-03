import datetime as dt
from django.db import models

from books.models import Book


class Document(models.Model):
    type = models.IntegerField(default=1)
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=300, null=True, blank=True)
    date = models.DateField(default=dt.date.today)
    is_order = models.BooleanField(default=False)


class Income(models.Model):
    book = models.ForeignKey(
        Book,
        on_delete=models.SET_NULL,
        null=True,
        related_name='incomes',
    )
    document = models.ForeignKey(
        Document,
        on_delete=models.SET_NULL,
        null=True,
        related_name='incomes',
    )
    count = models.IntegerField(default=0)
    part = models.IntegerField(default=0)
    price = models.FloatField(default=0)
    pub_year = models.IntegerField(default=dt.date.today().year)
    comment = models.CharField(max_length=80, null=True, blank=True)


class Outcome(models.Model):
    book_income = models.ForeignKey(
        Income,
        on_delete=models.SET_NULL,
        null=True,
        related_name='write_offs',
    )
    document = models.ForeignKey(
        Document,
        on_delete=models.SET_NULL,
        null=True,
        related_name='write_offs',
    )
    count = models.IntegerField(default=0)
    price = models.FloatField(default=0)
    comment = models.CharField(max_length=80)


class Exchange(models.Model):
    book = models.ForeignKey(
        Book,
        on_delete=models.SET_NULL,
        null=True,
        related_name='exchanges',
    )
    is_income = models.BooleanField(default=True)
    school = models.CharField(max_length=50)
    count = models.IntegerField(default=0)
    pub_year = models.IntegerField(default=dt.date.today().year)
    comment = models.CharField(max_length=80)


class Order(models.Model):
    book = models.ForeignKey(
        Book,
        on_delete=models.SET_NULL,
        null=True,
        related_name='orders',
    )
    document = models.ForeignKey(
        Document,
        on_delete=models.SET_NULL,
        null=True,
        related_name='orders',
    )
    count = models.IntegerField(default=0)
    price = models.FloatField(default=0)
    comment = models.CharField(max_length=80)


class Fund(models.Model):
    book = models.ForeignKey(
        Book,
        on_delete=models.SET_NULL,
        null=True,
        related_name='funds',
    )
    fund_count = models.IntegerField(default=0)
    overall_count = models.IntegerField(default=0)
