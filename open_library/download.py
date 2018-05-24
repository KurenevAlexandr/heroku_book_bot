"""Методы для скачивания """
import re
import pickle
import requests

from open_library.common import norm_title
# from common import norm_title # -- for WingIDE


def load_dict():
    """Выгружает словарь с заголовками"""
    return pickle.load(open("titles.p", "rb"))


def get_url_by_title(query, titles_to_urls=None):
    """Получает ссылку на книгу"""
    if titles_to_urls is None:
        titles_to_urls = load_dict()

    norm = norm_title(query)
    print(norm)
    try:
        url = titles_to_urls[query]
        return url
    except KeyError:
        return None


def download(link):
    """Скачивает книгу"""
    book_id = re.findall(r'\d+', link)[0]
    print('http://www.gutenberg.org/files/{}/{}.txt'.format(book_id, book_id))
    text = requests.get('http://www.gutenberg.org'
                        '/files/{}/{}.txt'.format(book_id,
                                                  book_id)).text[1000:3000]
    return text
