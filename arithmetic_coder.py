#!/usr/bin/env python

__author__ = 'Tomas Novacik'

from bitarray import bitarray


class ArithmeticCoder(object):

    def __init__(self, model):
        self.model = model

    def _init(self, output_type=bitarray):
        self.output = output_type()
        self.pending_bits = 0
        self.high = self.model.MAX_VAL
        self.low = self.model.MIN_VAL

    def _add_output_bits(self, bit):
        self.output.append(bit)
        for i in xrange(self.pending_bits):
            self.output.append(not bit)
        self.pending_bits = 0

    def _compress(self, input):
        symbol = self.model.get_interval(input)
        range = self.high - self.low + 1
        self.high = self.low + (range * symbol.high / symbol.count) - 1
        self.low = self.low + (range * symbol.low / symbol.count)

        while True:
            if self.high < self.model.ONE_HALF:
                self._add_output_bits(0)
            elif self.low >= self.model.ONE_HALF:
                self._add_output_bits(1)
            elif self.low >= self.model.ONE_FOURTH and\
                            self.high < self.model.THREE_FOURTHS:
                self.pending_bits += 1
                self.low -= self.model.ONE_FOURTH
                self.high -= self.model.ONE_FOURTH
            else:
              break

            self.high <<= 1
            self.high += 1
            self.low <<= 1
            self.high &= self.model.MAX_VAL
            self.low &= self.model.MAX_VAL

    def encode(self, data):
        self._init()

        for i in data:
            self._compress(i)

        # adding stop
        self._compress(self.model.EOF)

        if ( self.low < self.model.ONE_FOURTH ):
            self._add_output_bits(0)
        else:
            self._add_output_bits(1)
        return self.output.tobytes()

    def decode(self, data):
        input_bits = bitarray()
        input_bits.frombytes(data)
        input_bits.extend("1" * self.model.CODE_VALUE_BITS)
        value = 0

        start_index = min(self.model.CODE_VALUE_BITS, len(input_bits))

        self._init(list)

        for i in xrange(start_index):
            value <<= 1
            value += input_bits[i]

        index = start_index

        while index < len(input_bits):
            range = self.high - self.low + 1
            s_value =  ((value - self.low + 1) * self.model.get_count() - 1)
            s_value /= range
            symbol = self.model.get_symbol(s_value)

            if symbol.value == self.model.EOF:
                break
            self.output.append(symbol.value)
            self.high = self.low + (range*symbol.high)/symbol.count - 1
            self.low = self.low + (range*symbol.low)/symbol.count
            while True:
                if self.high < self.model.ONE_HALF:
                    pass
                elif self.low >= self.model.ONE_HALF:
                  value -= self.model.ONE_HALF
                  self.low -= self.model.ONE_HALF
                  self.high -= self.model.ONE_HALF
                elif self.low >= self.model.ONE_FOURTH and\
                                self.high < self.model.THREE_FOURTHS:
                  value -= self.model.ONE_FOURTH
                  self.low -= self.model.ONE_FOURTH
                  self.high -= self.model.ONE_FOURTH
                else:
                  break
                self.low <<= 1
                self.high <<= 1
                self.high += 1
                value <<= 1
                value += input_bits[index]
                index += 1

        return "".join(map(chr, self.output))

# eof
