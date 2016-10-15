#!/usr/bin/env python

__author__ = 'Tomas Novacik'

import unittest
import mock

from arithmetic_coder import ArithmeticCoder
from models import SimpleModel
from models import Symbol


class TestArithmeticCoder(unittest.TestCase):

    def setUp(self):
        self.ac = ArithmeticCoder(None)

    def test_coder(self):
        self.ac.model = SimpleModel()
        r_symbol = Symbol(1, 9, 15)
        self.ac.get_interval = mock.MagicMock(return_value=r_symbol)
        test_data = "aaaaaa"
        result = self.ac.encode(test_data)
        print result

if __name__ == "__main__":
    unittest.main()
# eof
