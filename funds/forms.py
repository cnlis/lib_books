import datetime as dt

from django import forms

from funds.calcs import parts_count
from funds.models import Fund, Document, Item
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


class IncomeList(forms.ModelForm):

    class Meta:
        model = Item
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


class NewIncomeDocument(forms.ModelForm):

    is_order = forms.BooleanField(
        label='Is order',
        required=False,
    )

    class Meta:
        model = Document
        fields = ('title', 'date', 'description')
        widgets = {
            'title': forms.Textarea(attrs={'rows': 1, 'cols': 15}),
            'description': forms.Textarea(attrs={'rows': 1, 'cols': 15}),
            'date': forms.SelectDateWidget(
                years=range(2010, dt.date.today().year+1),
                attrs={'style': 'width: auto; display: inline-block;'}
            ),
        }


class NewOutcomeDocument(forms.ModelForm):

    class Meta:
        model = Document
        fields = ('title', 'date', 'description')
        widgets = {
            'title': forms.Textarea(attrs={'rows': 1, 'cols': 15}),
            'description': forms.Textarea(attrs={'rows': 1, 'cols': 15}),
            'date': forms.SelectDateWidget(
                years=range(2010, dt.date.today().year+1),
                attrs={'style': 'width: auto; display: inline-block;'}
            ),
        }


class IncomeDetail(forms.ModelForm):

    class Meta:
        model = Item
        fields = ('book', 'part', 'count', 'price', 'pub_year', 'comment')
        widgets = {
            'part': forms.Select(choices=((0, 'Все'), (1, 1), (2, 2), (3, 3), (4, 4))),
            'count': forms.NumberInput(attrs={'min': 1, 'max': 500}),
            'price': forms.NumberInput(attrs={'min': 0, 'step': 0.01}),
            'pub_year': forms.NumberInput(
                attrs={'min': 2000, 'max': dt.date.today().year+1}
            ),
        }

    def clean(self):
        part = self.cleaned_data['part']
        item = self.cleaned_data['id']
        if part not in range(item.book.parts+1):
            raise forms.ValidationError('У учебника нет такой части!')
        return self.cleaned_data


class OutcomeDetail(forms.ModelForm):

    class Meta:
        model = Item
        fields = ('book', 'part', 'count', 'price', 'pub_year', 'comment')
        widgets = {
            'part': forms.Select(choices=((0, 'Все'), (1, 1), (2, 2), (3, 3), (4, 4))),
            'count': forms.NumberInput(attrs={'min': 1, 'max': 500}),
            'price': forms.NumberInput(attrs={'min': 0, 'step': 0.01}),
            'pub_year': forms.NumberInput(
                attrs={'min': 2000, 'max': dt.date.today().year + 1}
            ),
        }

    def clean(self):
        part = self.cleaned_data['part']
        item = self.cleaned_data['id']
        count = self.cleaned_data['count']
        fund_parts = parts_count(item.book, (1, 2), item.pk)
        if part not in range(item.book.parts+1):
            raise forms.ValidationError('У учебника нет такой части!')
        if count > fund_parts[part]:
            raise forms.ValidationError('Указанное количество превышает имеющееся!')
        return self.cleaned_data
