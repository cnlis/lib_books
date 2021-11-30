from django import forms

from books.models import Categorie, Klass


class SearchForm(forms.Form):
    categories = forms.ModelChoiceField(
        queryset=Categorie.objects.order_by('code'),
        label='Фильтр по категории:',
        required=False,
        empty_label='нет',
    )
    search = forms.CharField(
        label='Поиск по автору и названию:',
        required=False,
    )
    classes = forms.ChoiceField(
        choices=((i, i if i else 'нет') for i in range(0, 12)),
        label='Фильтр по классу:',
        required=False,
    )
    field_order = ['categories', 'search', 'classes']

