#!/usr/bin/env python

__author__ = 'Tomas Novacik'

import unittest
import tempfile

from models import SimpleModel

TEST_DATA = "baaaabbabcbcc"

class TestSimpleModel(unittest.TestCase):

    def setUp(self):
        self.mod = SimpleModel()

    def tearDown(self):
        self.mod = None

    def test_counts(self):
        self.mod.data = TEST_DATA
        self.mod._compute_symbol_counts()

        self.assertEqual(self.mod.total_count, len(TEST_DATA))
        e_symbols = [0] * self.mod.SYMBOL_COUNT

        for i in xrange(ord('a'), len(e_symbols)):
            e_symbols[i] += 5

        for i in xrange(ord('b'), len(e_symbols)):
            e_symbols[i] += 5

        for i in xrange(ord('c'), len(e_symbols)):
            e_symbols[i] += 3

        self.assertEqual(self.mod.symbols, e_symbols)
        symbol = self.mod.get_interval('b')

        e_low = 10
        e_high = 13

        self.assertEqual(symbol.low, e_low)
        self.assertEqual(symbol.high, e_high)
        self.assertEqual(symbol.count, len(TEST_DATA))

    def test_serialization(self):
        self.mod.data = TEST_DATA
        self.mod._compute_symbol_counts()
        handle, filename = tempfile.mkstemp()
        self.mod.save_to_file(filename)

        test_mod = SimpleModel()
        test_mod.load_from_file(filename)
        self.assertEqual(test_mod.symbols, self.mod.symbols)
        self.assertEqual(test_mod.total_count, self.mod.total_count)

if __name__ == '__main__':
    unittest.main()


# eof
