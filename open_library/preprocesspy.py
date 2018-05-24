"""Делает препроцессинг словаря заголовков"""
import pickle
from fuzzdict.dict import FuzzyDict
from pymarc import MARCReader
from common import norm_title


TITLES_TO_URLS = FuzzyDict()


def preprocess():
    """Препроцессинг таблицы заголовков"""
    file = open('catalog.marc', 'rb')
    reader = MARCReader(file)
    pickle.dump(TITLES_TO_URLS, open("titles1.p", "wb"))
    for record in reader:
        normtitle = norm_title(record.title())
        fields = record.as_dict()['fields']
        try:
            TITLES_TO_URLS[normtitle] = fields[-2]['856']['subfields'][0]['u']
            # print(titles_to_urls[normtitle])
        except KeyError:
            # print("--", d[-2]['830']['subfields'][0]['a'])
            try:
                TITLES_TO_URLS[normtitle] = fields[-2]['830']['subfields'][0]['a']
            except KeyError:
                print(record)
    pickle.dump(TITLES_TO_URLS, open("titles.p", "wb"))

if __name__ == '__main__':
    preprocess()
