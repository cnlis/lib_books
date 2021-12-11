from django.db.models import Q

from funds.models import Fund, Item


def parts_count(book, types, item_pk=None):
    items = Item.objects.select_related('book').filter(
        book=book,
        type__in=types
    ).all()
    if item_pk:
        items = items.filter(~Q(pk=item_pk))
    count = book.parts
    parts = [item.parts_count for item in items]
    parts_sum = [0] * (count + 1)
    for part in parts:
        if part:
            parts_sum = [i1 + i2 for i1, i2 in zip(parts_sum, part)]
    parts_sum[0] = min(parts_sum[1:])
    return parts_sum


def sum_fund():
    income_list = Item.objects.select_related('book').filter(type=1).values_list('book')
    for income in income_list:
        Fund.objects.get_or_create(book_id=income[0])
    fund_list = Fund.objects.select_related('book').all()
    for book in fund_list:
        fund_parts = parts_count(book.book, (1, 2))
        overall_parts = parts_count(book.book, (1, 2, 3, 4))
        order_parts = parts_count(book.book, (5,))
        outcome_parts = parts_count(book.book, (2,))
        exchange_parts = parts_count(book.book, (3, 4))

        book.fund_count = fund_parts[0]
        book.overall_count = overall_parts[0]
        book.order_count = order_parts[0]
        book.outcome_count = outcome_parts[0]
        book.exchange_count = exchange_parts[0]
        book.records_count = Item.objects.filter(book=book.book).count()
        book.save()
