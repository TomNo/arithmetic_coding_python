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

    def test_serialization(self):
        self.mod.data = TEST_DATA
        self.mod._compute_symbol_counts()
        handle, filename = tempfile.mkstemp()
        self.mod.save_to_file(filename)

        test_mod = SimpleModel()
        test_mod.load_from_file(filename)
        self.assertEqual(test_mod.symbols, self.mod.symbols)

if __name__ == '__main__':
    unittest.main()


# eof
