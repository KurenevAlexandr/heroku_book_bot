from numpy import random as rand
import random


class Histogram(dict):
    def __init__(self, iterable=None):
        super().__init__()
        self.num_of_distinct = 0
        self.tokens_num = 0
        if iterable:
            self.update(iterable)

    def update(self, iterable):
        for token in iterable:
            if token in self:
                self[token] += 1
                self.tokens_num += 1
            else:
                self[token] = 1
                self.num_of_distinct += 1
                self.tokens_num += 1

    def frequency(self, token):
        res = self.get(token)
        assert res
        return res

    def get_random(self):
        return rand.sample(self, 1)[0]

    def get_weighted_random(self):
        tokens_list = self.keys()
        rand_weight = rand.randint(0, self.tokens_num, 1)
        for token in tokens_list:
            rand_weight = rand_weight - self[token]
            if rand_weight <= 0:
                return token


class MarkovModel(dict):
    def __init__(self):
        dict().__init__(self)

    def update_model(self, model_order, data):
        for i in range(0, len(data) - model_order):
            slider = tuple(data[i:i + model_order])
            if slider in self:
                self[slider].update([data[i + model_order]])
            else:
                self[slider] = Histogram([data[i + model_order]])

    def random_sent(self, length, seed_word):
        keys = set(self)
        seed = None
        if seed_word is None:
            seed = rand.choice(list(keys))
        else:
            seed = (seed_word,)
        sent = [*seed]
        while (len(sent) < length):
            current_hist = self[seed]
            gen = current_hist.get_weighted_random()
            sent.append(gen)
            seed = gen if gen in keys else rand.choice(list(keys))
        return " ".join(sent)
