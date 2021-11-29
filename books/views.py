import operator
from functools import reduce

from django.shortcuts import render
from django.db.models import Q

from .models import Book, Categorie, Klass


def books_index(request):
    input_search = ''
    input_classes = 0
    input_categories = ''
    books = Book.objects.select_related(
        'classes',
        'publisher',
        'language',
        'special',
    ).all()
    if request.method == 'POST':
        if request.POST.get('search'):
            input_search = request.POST.get('search')
            search_list = input_search.split()
            books = books.filter(
                reduce(operator.and_,
                       (Q(author__contains=q) for q in search_list)) |
                reduce(operator.and_,
                       (Q(title__contains=q) for q in search_list))
            )
        if request.POST.get('classes'):
            input_classes = int(request.POST.get('classes'))
            books = books.filter(classes__pk=input_classes).all()
        if request.POST.get('categories'):
            input_categories = request.POST.get('categories')
            books = books.filter(code__startswith=input_categories).all()
    classes = Klass.objects.order_by('class_from').all()
    categories = Categorie.objects.order_by('code').all()
    context = {
        'books': books[:100],
        'classes': classes,
        'categories': categories,
        'input_search': input_search,
        'input_classes': input_classes,
        'input_categories': input_categories,
    }
    return render(request, 'books/index.html', context)
