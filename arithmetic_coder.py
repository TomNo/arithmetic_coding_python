#!/usr/bin/env python

__author__ = 'Tomas Novacik'

from bitarray import bitarray


class ArithmeticCoder(object):

    def __init__(self, model):
        self.model = model
        self._init()

    def _init(self):
        self.output = bitarray()
        self.pending_bits = 0

    def _add_output_bits(self, bit):
        self.output.append(bit)
        for i in xrange(self.pending_bits):
            self.output.append(not bit)
        self.pending_bits = 0

    def encode(self, data):
        high = self.model.MAX_VAL
        low = self.model.MIN_VAL

        self._init()

        for i in data:
            symbol = self.model.get_interval(i)
            range = high - low + 1
            high = low + (range * symbol.high / symbol.count) - 1
            low = low + (range * symbol.low / symbol.count)

            while True:
                if high < self.model.ONE_HALF:
                    self._add_output_bits(0)
                elif low >= self.model.ONE_HALF:
                    self._add_output_bits(1)
                elif low >= self.model.ONE_FOURTH and\
                                high < self.model.THREE_FOURTHS:
                    self.pending_bits += 1
                    low -= self.model.ONE_FOURTH
                    high -= self.model.ONE_FOURTH
                else:
                  break

                high <<= 1
                high += 1
                low <<= 1
                high &= self.model.MAX_VAL
                low &= self.model.MAX_VAL

                if ( low < self.model.ONE_FOURTH ):
                    self._add_output_bits(0)
                else:
                    self._add_output_bits(1)

        return self.output.tobytes()

    def decode(self, data):
        high = self.model.MAX_VAL
        low = self.model.MIN_VAL

        value = 0
        start_index = min(self.model.CODE_VALUE_BITS, len(data))

        self._init()

        for i in xrange(start_index):
            value <<= 1
            value += 0 if data[i] == '0' else 1

        index = start_index

        while index < len(data):
            range = high - low + 1
            scaled_value =  ((value - low + 1) * self.model.get_count() - 1 )
            scaled_value /= range
            symbol = self.model.get_symbol(scaled_value)

            if symbol.value == 256:
                break
            self.output.append(symbol.value)

            high = low + (range*symbol.high)/symbol.count - 1
            low = low + (range*symbol.low)/symbol.count

        while True:
            if high < self.model.ONE_HALF:
                pass
            elif low >= self.model.ONE_HALF:
              value -= self.model.ONE_HALF
              low -= self.model.ONE_HALF
              high -= self.model.ONE_HALF
            elif low >= self.model.ONE_FOURTH and\
                            high < self.model.THREE_FOURTHS:
              value -= self.model.ONE_FOURTH
              low -= self.model.ONE_FOURTH
              high -= self.model.ONE_FOURTH
            else:
              break
            low <<= 1
            high <<= 1
            high += 1
            value <<= 1
            value += 1 if data[index] == '1' else 0
            index += 1

        return self.output.tobytes()

# eof
