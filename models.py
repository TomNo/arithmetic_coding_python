#!/usr/bin/env python

__author__ = 'Tomas Novacik'


import json

class Symbol(object):

    def __init__(self, low, high, count, value=None):
        self.low = low
        self.high = high
        self.count = count
        self.value = value

    def __str__(self):
        return str({"low": self.low, "high": self.high, "count": self.count,
                    "value": self.value})


class Model(object):
    """Base class for statistical model of the input data"""

    CODE_VALUE_BITS = 16
    FREQUENCY_BITS = 14
    MAX_VAL = (1 << CODE_VALUE_BITS) - 1
    MIN_VAL = 0
    # max count after which the counting is stopped
    MAX_FREQ = (1 << FREQUENCY_BITS) - 1
    ONE_FOURTH    = (1 << (CODE_VALUE_BITS - 2))
    ONE_HALF      = 2 * ONE_FOURTH
    THREE_FOURTHS = 3 * ONE_FOURTH

    SYMBOL_COUNT = 258  # range of byte + EOF

    EOF = 256 # end of encoded input

    def __init__(self):
        self.symbols = range(self.SYMBOL_COUNT)

    def get_interval(self, symbol):
        """Returns the interval for given symbol and total count of symbols."""
        if type(symbol) == str:
            index = ord(symbol)
        else:
            index = symbol

        symbol = Symbol(self.symbols[index], self.symbols[index+1],
                        self.get_count())
        return symbol

    def get_count(self):
        return self.symbols[-1]

    def get_symbol(self, scaled_value):
        for i in xrange(self.SYMBOL_COUNT - 1):
            if scaled_value < self.symbols[i+1]:
                return Symbol(self.symbols[i], self.symbols[i+1],
                              self.get_count(), i)

    def load_from_file(self, filename):
        """Loads model from path - expecting json"""
        with open(filename, "r") as input_file:
            obj = json.load(input_file)
            self.symbols = obj["symbols"]

    def save_to_file(self, filename):
        with open(filename, "w") as output_file:
            obj = {"symbols": self.symbols}
            json.dump(obj, output_file)


class SimpleModel(Model):
    """Very simple model that computes probabilities from the input data and
    must be present in the decompression process"""

    def __init__(self, data=None):
        super(SimpleModel, self).__init__()
        if data is not None:
            self.data = data
            self._compute_symbol_counts()

    def _compute_symbol_counts(self):
        """TODO this is just simple realization that should not break the
        logic for better models"""
        for i in self.data:
            for i in xrange(ord(i) + 1, self.SYMBOL_COUNT):
                self.symbols[i] += 1

            if self.get_count() >= self.MAX_FREQ:
                break

class AdaptiveModel(Model):
    """Module that computes probabilities on the fly."""

    def __init__(self):
        super(AdaptiveModel, self).__init__()
        self.frozen = False

    def _update(self, symbol):
        # in case we get EOF or counts are already frozen => do nothing
        if self.frozen:
            return

        if type(symbol) != str:
            index = symbol
        else:
            index = ord(symbol)

        for i in xrange(index + 1, self.SYMBOL_COUNT):
            self.symbols[i] += 1

        if self.symbols[-1] > self.MAX_FREQ:
            self.frozen = True

    def get_symbol(self, scaled_value):
        symbol = super(AdaptiveModel, self).get_symbol(scaled_value)
        self._update(symbol.value)
        return symbol

    def get_interval(self, symbol):
        result = super(AdaptiveModel, self).get_interval(symbol)
        self._update(symbol)
        return result


# eof
