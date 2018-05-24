"""Слоаврь с примерным поиском слов"""
import difflib

class FuzzyDict(dict):
    "Provides a dictionary that performs fuzzy lookup"
    def __init__(self, items=None, cutoff=0.6):
        """Инициализация словаря"""
        super(FuzzyDict, self).__init__()

        if items:
            self.update(items)
        self.cutoff = cutoff

    def contains(self, key):
        """Метод-обертка"""
        return super(FuzzyDict, self).__contains__(key)

    def get_item(self, key):
        """Метод-обертка"""
        return super(FuzzyDict, self).__getitem__(key)

    def _search(self, lookfor, stop_on_first=False):
        """Возвращает элемент"""
        if self.contains(lookfor):
            return True, lookfor, self.get_item(lookfor), 1

        ratio_calc = difflib.SequenceMatcher()
        ratio_calc.set_seq1(lookfor)

        best_ratio = 0.0
        best_match = None
        best_key = None
        for key in self:
            try:
                ratio_calc.set_seq2(key)
            except TypeError:
                continue
            try:
                ratio = ratio_calc.ratio()
            except TypeError:
                break

            if ratio > best_ratio:
                best_ratio = ratio
                best_key = key
                best_match = self.get_item(key)

            if stop_on_first and ratio >= self.cutoff:
                break

        return (
            best_ratio >= self.cutoff,
            best_key,
            best_match,
            best_ratio)


    def __contains__(self, item):
        """Перегружает стд метод"""
        return bool(self._search(item, True)[0])

    def __getitem__(self, lookfor):
        """Перегружает стд метод"""
        matched, _, item, _ = self._search(lookfor)

        if not matched:
            return item

        return item
