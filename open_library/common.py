"""Полезные функции для работы с заголовками"""
import re


def norm_word(word):
    """Нормализует слово"""
    return re.sub(r'[\W]', '', word.lower())


def norm_title(title):
    """Нормализует заголовок"""
    return " ".join([norm_word(word) for word in title.split()])
