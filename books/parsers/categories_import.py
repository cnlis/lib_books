import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

from books.models import Category


def category_parser():
    data = []
    r = requests.get('https://fpu.edu.ru/')
    soup = BeautifulSoup(r.content, 'lxml')
    lst = soup.find(
        name='select',
        attrs={'id': 'subjectAll', 'name': 'subjectAll'},
    ).find_all('optgroup')
    categories_lst = []
    for i in lst:
        categories_lst.append('..'+i['label'])
        for j in i.children:
            if j.name == 'option':
                categories_lst.append('..'+j.text)
    index = [0]*6
    prev_level = 0
    for item in categories_lst:
        category = item.split('..')
        level = category.count('')
        if level < prev_level:
            for i in range(prev_level-level):
                index[prev_level-i] = 0
        index[level] += 1
        index_str = '.'.join(str(i) for i in index if i)
        prev_level = level
        data.append((index_str, category[-1]))
    return data


def category_saver(categories_list):
    for item in tqdm(categories_list):
        Category.objects.create(
            code=item[0],
            title=item[1]
        )
