from django.db.models import Q
from django.forms import modelformset_factory
from django.http import JsonResponse
from django.shortcuts import render, redirect

from funds.calcs import sum_fund, parts_count
from funds.models import Fund, Document, Item
from books.models import Book
from funds.forms import FundList, NewIncomeDocument, IncomeDetail, NewOutcomeDocument, OutcomeDetail, IncomeList


def book_ajax_query(t):
    return Book.objects.filter(
        Q(author__contains=t) |
        Q(title__contains=t) |
        Q(grades__title__contains=t)
    ).all()


def item_ajax_query(t):
    return Item.objects.select_related('book').filter(type=1).filter(
        Q(book__author__contains=t) |
        Q(book__title__contains=t) |
        Q(book__grades__title__contains=t)
    ).all()


def ajax_response(request, queryset):
    term = request.GET.get('term').split()
    for t in term:
        books = queryset(t)
    lst = []
    for pk, text in zip(books.values_list('pk', flat=True), books):
        lst.append({'id': pk, 'text': str(text)})
    return JsonResponse(lst, safe=False)


def funds_index(request):
    sum_fund()
    funds = Fund.objects.select_related(
        'book',
    ).all().order_by('book__grades', 'book__code')
    form = FundList(request.POST or None)
    if request.is_ajax():
        return ajax_response(request, book_ajax_query)
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
    docs = Document.objects.filter(type__in=(1, 5)).order_by('-date').all()
    form = NewIncomeDocument(request.POST or None)
    if request.method == 'POST':
        is_order = request.POST.get('is_order')
        if form.is_valid():
            data = form.save(commit=False)
            if is_order:
                data.type = 5 if is_order else 1
            data.save()
    context = {
        'docs': docs,
        'form': form,
    }
    return render(request, template, context)


def funds_income_detail(request, doc_id):
    template = 'funds/income_detail.html'
    IncomeSet = modelformset_factory(Item, form=IncomeDetail, extra=0)
    doc = Document.objects.get(pk=doc_id)
    doc_data = doc.item_set.filter(type=doc.type).all()
    formset = IncomeSet(queryset=doc_data)
    form = FundList()
    if request.is_ajax():
        return ajax_response(request, book_ajax_query)
    if request.method == 'POST':
        if 'submit' in request.POST:
            book = Book.objects.get(pk=request.POST.get('book'))
            Item.objects.create(
                type=doc.type,
                book=book,
                document=doc,
            )
        if 'save' in request.POST:
            formset = IncomeSet(request.POST)
            if formset.is_valid():
                for form in formset:
                    if form.is_valid():
                        form.save()
            else:
                return render(request, template, {'formset': formset, 'form': form, 'doc_id': doc_id,})
        return redirect('funds:income_detail', doc_id=doc_id)
    context = {
        'formset': formset,
        'form': form,
        'doc_id': doc_id,
    }
    return render(request, template, context)


def funds_income_edit(request, doc_id):
    template = 'funds/income_edit.html'
    document = Document.objects.get(pk=doc_id)
    form = NewIncomeDocument(request.POST or None, instance=document)
    form.fields['is_order'].initial = (document.type == 5)
    context = {
        'form': form,
    }
    if request.method == 'POST':
        is_order = request.POST.get('is_order')
        if form.is_valid():
            data = form.save(commit=False)
            data.type = 5 if is_order else 1
            data.save()
            items = Item.objects.filter(document=document).all()
            for item in items:
                item.type = data.type
                item.save()
        return redirect('funds:income_list')
    return render(request, template, context)


def funds_income_del(request, doc_id):
    Document.objects.filter(pk=doc_id).delete()
    return redirect('funds:income_list')


def funds_income_book_del(request, doc_id, record_id):
    Item.objects.filter(pk=record_id).delete()
    return redirect('funds:income_detail', doc_id=doc_id)


def funds_book_detail(request, book_id):
    template = 'funds/book_detail.html'
    item = Fund.objects.select_related('book').get(pk=book_id)
    income_docs = Item.objects.select_related('book', 'document').filter(
        type=1,
        book=item.book_id,
    ).all()
    outcome_docs = Item.objects.select_related('book', 'document').filter(
        type=2,
        book=item.book_id).all()
    exchange_docs = Item.objects.select_related('book').filter(
        type__in=(3, 4),
        book=item.book_id).all()
    parts = parts_count(item.book, (1, 2, 3, 4))

    context = {
        'book': item,
        'income_docs': income_docs,
        'outcome_docs': outcome_docs,
        'exchange_docs': exchange_docs,
        'parts': parts,
    }
    return render(request, template, context)


def funds_outcome_list(request):
    template = 'funds/outcome_list.html'
    docs = Document.objects.filter(type=2).order_by('-date').all()
    form = NewOutcomeDocument(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            record = form.save(commit=False)
            record.type = 2
            record.save()
    context = {
        'docs': docs,
        'form': form,
    }
    return render(request, template, context)


def funds_outcome_detail(request, doc_id):
    template = 'funds/outcome_detail.html'
    OutcomeSet = modelformset_factory(Item, form=OutcomeDetail, extra=0)
    doc = Document.objects.get(pk=doc_id)
    doc_data = doc.item_set.filter(type=2).all()
    formset = OutcomeSet(queryset=doc_data)
    form = IncomeList()
    if request.is_ajax():
        return ajax_response(request, item_ajax_query)
    if request.method == 'POST':
        if 'submit' in request.POST:
            item = Item.objects.get(pk=request.POST.get('book'))
            record = Item.objects.create(
                type=2,
                book=item.book,
                document=doc,
            )
            record.count = item.count
            record.part = item.part
            record.pub_year = item.pub_year
            record.price = item.price
            record.save()
        if 'save' in request.POST:
            formset = OutcomeSet(request.POST)
            if formset.is_valid():
                for form in formset:
                    if form.is_valid():
                        form.save()
            else:
                return render(request, template, {'formset': formset, 'form': form, 'doc_id': doc_id})
        return redirect('funds:outcome_detail', doc_id=doc_id)
    context = {
        'formset': formset,
        'form': form,
        'doc_id': doc_id,
    }
    return render(request, template, context)


def funds_outcome_edit(request, doc_id):
    template = 'funds/outcome_edit.html'
    document = Document.objects.get(pk=doc_id)
    form = NewOutcomeDocument(request.POST or None, instance=document)
    context = {
        'form': form
    }
    if request.method == 'POST':
        if form.is_valid():
            form.save()
        return redirect('funds:outcome_list')
    return render(request, template, context)


def funds_outcome_del(request, doc_id):
    Document.objects.filter(pk=doc_id).delete()
    return redirect('funds:outcome_list')


def funds_outcome_book_del(request, doc_id, record_id):
    Item.objects.filter(pk=record_id).delete()
    return redirect('funds:outcome_detail', doc_id=doc_id)
