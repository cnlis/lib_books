import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


from books.models import Book, Klass, Language, Publisher, Source, Special


def books_parser(pages_count):
    data = []
    for page_num in tqdm(range(1, pages_count+1)):
        r = requests.get(f'https://fpu.edu.ru/?submit=&page={page_num}')
        soup = BeautifulSoup(r.content, 'lxml')
        lst = soup.find(
            name='div',
            attrs={'class': 'divTable'}
        ).find_all('div', attrs={'class': 'divTableRow'})
        for i, row in enumerate(lst):
            if not i:
                continue
            s = []
            special = '-'
            for cell in row.find_all(
                    'div',
                    attrs={'class': 'divTableCell'}
            ):
                s.append(cell.text.strip())
                if cell.find('div'):
                    special = cell.find('div').find('span').text.strip()
                    s[-1] = s[-1][:-len(special)-1].strip()
            s.append(special)
            data.append(s)
    return data


def books_saver(books_list, source):
    class_set = {}
    language_set = {}
    publisher_set = {}
    special_set = {}
    source = Source.objects.get_or_create(title=source)
    for item in books_list:
        class_set[item[3]] = 0
        language_set[item[5]] = 0
        publisher_set[item[4]] = 0
        special_set[item[6]] = 0
    for item in class_set:
        class_from, class_to, suffix = Klass.parse_string(item)
        class_set[item] = Klass.objects.get_or_create(
            class_from=class_from,
            class_to=class_to,
            suffix=suffix
        )
    for item in language_set:
        language_set[item] = (
            Language.objects.get_or_create(title=item)
            if item else Language.objects.get_or_create(pk=1)
        )
    for item in publisher_set:
        publisher_set[item] = (
            Publisher.objects.get_or_create(title=item)
            if item else Publisher.objects.get_or_create(pk=1)
        )
    for item in special_set:
        special_set[item] = (Special.objects.get_or_create(title=item)
                             if item else Special.objects.get_or_create(pk=1))
    for item in tqdm(books_list):
        Book.objects.create(
            source=source[0],
            code=item[0],
            title=item[1],
            author=item[2],
            classes=class_set[item[3]][0],
            publisher=publisher_set[item[4]][0],
            language=language_set[item[5]][0],
            special=special_set[item[6]][0]
        )
