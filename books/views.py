import operator
from functools import reduce

from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render
from django.db.models import Q
from django.shortcuts import redirect

from books.models import Book, Category, Grade
from books.forms import SearchForm, DetailBook, AddClasses


BOOKS_COUNT = 15


def create_paginator(request, post_list):
    paginator = Paginator(post_list, BOOKS_COUNT)
    page_number = request.GET.get('page') or 1
    return (paginator.get_page(number=page_number),
            paginator.get_elided_page_range(number=page_number))


def books_index(request):
    books = Book.objects.select_related(
        'grades',
        'publisher',
        'language',
        'special',
    ).order_by('code').all()
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
        input_classes = request.POST.get('grades')
        if int(input_classes):
            books = books.filter(
                grades__title__contains=input_classes
            )
        input_category = request.POST.get('categories')
        if input_category:
            category = Category.objects.get(pk=input_category)
            books = books.filter(code__startswith=category.code).all()
    page_obj, pages = create_paginator(request, books)
    context = {
        'page_obj': page_obj,
        'pages': pages,
        'form': form,
    }
    return render(request, 'books/index.html', context)


def books_detail(request, book_id):
    book = Book.objects.get(pk=book_id)
    form = DetailBook(request.POST or None, instance=book)
    if request.is_ajax():
        term = request.GET.get('term')
        classes = Grade.objects.filter(title__contains=term).all()
        return JsonResponse(list(classes.values()), safe=False)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('books:detail', book_id=book_id)
    context = {
        'book_id': book_id,
        'form': form,
    }
    return render(request, 'books/detail.html', context)


def create_classes(request):
    form = AddClasses()
    context = {
        'form': form,
    }
    return render(request, 'books/detail.html', context)
