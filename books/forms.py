from django import forms

from books.models import Book, Category, Grade


class SearchForm(forms.Form):
    categories = forms.ModelChoiceField(
        queryset=Category.objects.order_by('code'),
        label='Фильтр по категории:',
        required=False,
        empty_label='нет',
    )
    search = forms.CharField(
        label='Поиск по автору и названию:',
        required=False,
    )
    grades = forms.ChoiceField(
        choices=((i, i if i else 'нет') for i in range(0, 12)),
        label='Фильтр по классу:',
        required=False,
    )
    field_order = ['categories', 'search', 'grades']


class DetailBook(forms.ModelForm):

    class Meta:
        model = Book
        fields = '__all__'
        widgets = {
            'author': forms.Textarea(attrs={'rows': 3, 'cols': 15}),
            'title': forms.Textarea(attrs={'rows': 3, 'cols': 15}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['grades'].queryset = Grade.objects.none()

        if 'grades' in self.data:
            self.fields['grades'].queryset = Grade.objects.all()
        elif self.instance.pk:
            self.fields['grades'].queryset = Grade.objects.all().filter(
                pk=self.instance.grades.pk
            )


class AddClasses(forms.ModelForm):

    class Meta:
        model = Grade
        fields = '__all__'
