import operator
from functools import reduce

from django.http import JsonResponse
from django.shortcuts import render
from django.db.models import Q
from django.shortcuts import redirect

from books.models import Book, Category, Grade
from books.forms import SearchForm, DetailBook, AddClasses


def books_index(request):
    books = Book.objects.select_related(
        'grades',
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
        input_classes = request.POST.get('grades')
        if int(input_classes):
            books = books.filter(
                grades__title__contains=input_classes
            )
        input_category = request.POST.get('categories')
        if input_category:
            category = Category.objects.get(pk=input_category)
            books = books.filter(code__startswith=category.code).all()
    context = {
        'books': books[:100],
        'form': form,
    }
    return render(request, 'books/index.html', context)


def books_detail(request, book_id):
    book = Book.objects.get(pk=book_id)
    form = DetailBook(request.POST or None, instance=book)
    if request.is_ajax():
        term = request.GET.get('term')
        classes = Grade.objects.filter(title__contains=term).all()
        print(classes.values())
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
