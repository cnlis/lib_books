import datetime as dt
from django.db import models

from books.models import Book


class Document(models.Model):
    type = models.IntegerField(default=1)
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=300, null=True, blank=True)
    date = models.DateField(default=dt.date.today)


class Item(models.Model):
    document = models.ForeignKey(
        Document,
        on_delete=models.SET_NULL,
        null=True,
    )
    book = models.ForeignKey(
        Book,
        on_delete=models.SET_NULL,
        null=True,
    )
    type = models.IntegerField(default=1)
    count = models.IntegerField(default=0)
    part = models.IntegerField(default=0)
    price = models.FloatField(default=0)
    pub_year = models.IntegerField(default=dt.date.today().year)
    comment = models.CharField(max_length=80, null=True, blank=True)
    school = models.CharField(max_length=50, null=True, blank=True)

    @property
    def parts_count(self):
        count = self.count
        if self.type in (2, 4):
            count = -count
        if not self.part:
            result = [count] * (self.book.parts + 1)
        else:
            result = [0] * (self.book.parts + 1)
            result[self.part] = count
        return result

    def __str__(self):
        part = ' - (все части)' if not self.part else f' - (часть {self.part})'
        return (f'{self.book}{part} - {self.count} экз. - {self.pub_year} - '
                f'{self.price:.2f} руб.')


class Fund(models.Model):
    book = models.ForeignKey(
        Book,
        on_delete=models.SET_NULL,
        null=True,
        related_name='funds',
    )
    fund_count = models.IntegerField(default=0)
    overall_count = models.IntegerField(default=0)
    exchange_count = models.IntegerField(default=0)
    order_count = models.IntegerField(default=0)
    pupils = models.IntegerField(default=0)
    records_count = models.IntegerField(default=0)

    @property
    def fund_parts(self):
        pass

    def __str__(self):
        return f'{self.book} - в фонде {self.fund_count} экз.'
