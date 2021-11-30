import operator
from functools import reduce

from django.shortcuts import render
from django.db.models import Q

from books.models import Book, Categorie, Klass
from books.forms import SearchForm


def books_index(request):
    books = Book.objects.select_related(
        'classes',
        'publisher',
        'language',
        'special',
    ).all()
    form = SearchForm(request.POST or None)
    if request.method == 'POST':
        search_list = request.POST.get('search').split()
        if search_list:
            books = books.filter(
                reduce(operator.and_,
                       (Q(author__contains=q) for q in search_list)) |
                reduce(operator.and_,
                       (Q(title__contains=q) for q in search_list))
            )
        input_classes = request.POST.get('classes')
        if int(input_classes):
            books = books.filter(
                Q(classes__class_from=int(input_classes)) |
                Q(classes__class_to=int(input_classes))
            )
        input_category = request.POST.get('categories')
        if input_category:
            category = Categorie.objects.get(pk=input_category)
            books = books.filter(code__startswith=category.code).all()
    context = {
        'books': books[:100],
        'form': form,
    }
    return render(request, 'books/index.html', context)
