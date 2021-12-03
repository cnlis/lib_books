import datetime as dt

from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator

from funds.models import Fund, Document, Income
from books.models import Book


class FundList(forms.ModelForm):

    class Meta:
        model = Fund
        fields = ('book',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['book'].queryset = Book.objects.none()

        if 'book' in self.data:
            self.fields['book'].queryset = Book.objects.all()
        elif self.instance.pk:
            self.fields['book'].queryset = Book.objects.all().filter(
                pk=self.instance.book.pk
            )


class NewDocument(forms.ModelForm):

    class Meta:
        model = Document
        fields = ('title', 'date', 'description', 'is_order')
        widgets = {
            'title': forms.Textarea(attrs={'rows': 1, 'cols': 15}),
            'description': forms.Textarea(attrs={'rows': 1, 'cols': 15}),
            'date': forms.SelectDateWidget(years=range(2010, dt.date.today().year+1)),
            'is_order': forms.CheckboxInput()
        }


class IncomeDetail(forms.ModelForm):

    class Meta:
        model = Income
        fields = ('book', 'part', 'count', 'price', 'pub_year', 'comment')
        widgets = {
            'part': forms.NumberInput(attrs={'min': 0, 'max': 4}),
            'count': forms.NumberInput(attrs={'min': 0, 'max': 500}),
            'price': forms.NumberInput(attrs={'min': 0, 'step': 0.01}),
            'pub_year': forms.NumberInput(
                attrs={'min': 2000, 'max': dt.date.today().year+1}
            ),
        }

class IncomeDetailWithOutBook(forms.ModelForm):

    class Meta:
        model = Income
        fields = ('part', 'count', 'price', 'pub_year', 'comment')