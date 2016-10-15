#!/usr/bin/env python

__author__ = 'Tomas Novacik'


import json
import math
import sys

class Symbol(object):

    def __init__(self, low, high, count, value=None):
        self.low = low
        self.high = high
        self.count = count
        self.value = value

    def __str__(self):
        return str({"low": self.low, "high": self.high, "count": self.count})


class Model(object):
    """Base class for statistical model of the input data"""

    MAX_VAL = sys.maxsize
    MIN_VAL = 0
    CODE_VALUE_BITS = int(math.log(MAX_VAL, 2))
    # max count after which the counting is stopped
    MAX_FREQ = (1 << (CODE_VALUE_BITS - 4))
    ONE_FOURTH    = (1 << (CODE_VALUE_BITS - 2))
    ONE_HALF      = 2 * ONE_FOURTH
    THREE_FOURTHS = 3 * ONE_FOURTH

    SYMBOL_COUNT = 257  # range of byte + EOF

    def __init__(self, data=None):
        self.data = data
        self.symbols = [0] * self.SYMBOL_COUNT
        self.total_count = 0

    def get_interval(self, symbol):
        """Returns the interval for given symbol and total count of symbols."""
        index = ord(symbol)
        symbol = Symbol(self.symbols[index], self.symbols[index+1],
                        self.total_count)
        return symbol

    def get_count(self):
        return self.total_count

    def get_symbol(self, scaled_value):
        for i in xrange(self.SYMBOL_COUNT - 1):
            if scaled_value < self.symbols[i+1]:
                return Symbol(self.symbols[i], self.symbols[i+1],
                              self.total_count, i)

    def load_from_file(self, filename):
        """Loads model from path - expecting json"""
        with open(filename, "r") as input_file:
            obj = json.load(input_file)
            self.total_count = obj["total_count"]
            self.symbols = obj["symbols"]

    def save_to_file(self, filename):
        with open(filename, "w") as output_file:
            obj = {"symbols": self.symbols, "total_count": self.total_count}
            json.dump(obj, output_file)


class SimpleModel(Model):
    """Very simple model that computes probabilities from the input data and
    must be present in the decompression process"""

    def __init__(self, data=None):
        super(SimpleModel, self).__init__(data)
        if data is not None:
            self._compute_symbol_counts()

    def _compute_symbol_counts(self):
        for i in self.data:
            for i in xrange(ord(i), self.SYMBOL_COUNT):
                self.symbols[i] += 1
            self.total_count += 1

            if self.total_count >= self.MAX_FREQ:
                break


# eof
