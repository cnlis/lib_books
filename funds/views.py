import operator

import django.forms
from django.db.models import Q
from django.forms import modelformset_factory
from django.http import JsonResponse
from django.shortcuts import render, redirect

from funds.models import Fund, Document, Income
from books.models import Book
from funds.forms import FundList, NewDocument, IncomeDetail, \
    IncomeDetailWithOutBook


def ajax_book_response(request):
    term = request.GET.get('term').split()
    books = Book.objects.all()
    for t in term:
        books = books.filter(
            Q(author__contains=t) |
            Q(title__contains=t) |
            Q(grades__title__contains=t)
        ).all()
    lst = []
    for pk, text in zip(books.values_list('pk', flat=True), books):
        lst.append({'id': pk, 'text': str(text)})
    return JsonResponse(lst, safe=False)


def funds_index(request):
    funds = Fund.objects.select_related(
        'book',
    ).all()
    form = FundList(request.POST or None)
    if request.is_ajax():
        return ajax_book_response(request)
    if request.method == 'POST':
        book = Book.objects.get(pk=request.POST.get('book'))
        Fund.objects.get_or_create(
            book=book
        )
        return redirect('funds:index')
    context = {
        'form': form,
        'funds': funds,
    }
    return render(request, 'funds/index.html', context)


def funds_income_list(request):
    template = 'funds/income_list.html'
    docs = Document.objects.filter(type=1).order_by('-date').all()
    form = NewDocument(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
    context = {
        'docs': docs,
        'form': form,
    }
    return render(request, template, context)


def funds_income_detail(request, doc_id):
    template = 'funds/income_detail.html'
    IncomeSet = modelformset_factory(Income, form=IncomeDetail, extra=0)
    doc = Document.objects.get(pk=doc_id)
    doc_data = doc.incomes.all()
    formset = IncomeSet(queryset=doc_data)
    form = FundList(request.POST or None)
    if request.is_ajax():
        return ajax_book_response(request)
    if request.method == 'POST':
        if 'submit' in request.POST:
            print(request.POST)
            book = Book.objects.get(pk=request.POST.get('book'))
            Income.objects.get_or_create(
                book=book,
                document=doc,
            )
        if 'save' in request.POST:
            # book field is not render
            IncomeSet = modelformset_factory(
                Income,
                form=IncomeDetailWithOutBook,
                extra=0
            )
            formset = IncomeSet(request.POST)
            if formset.is_valid():
                for form in formset:
                    if form.is_valid():
                        form.save()
        return redirect('funds:income_detail', doc_id=doc_id)
    context = {
        'formset': formset,
        'form': form,
        'doc_id': doc_id,
    }
    return render(request, template, context)


def funds_income_del(request, doc_id):
    Document.objects.filter(pk=doc_id).delete()
    return redirect('funds:income_list')


def funds_income_book_del(request, doc_id, record_id):
    Income.objects.filter(pk=record_id).delete()
    return redirect('funds:income_detail', doc_id=doc_id)
