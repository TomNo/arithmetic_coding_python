#!/usr/bin/env python

__author__ = 'Tomas Novacik'

import unittest

import models

from arithmetic_coder import ArithmeticCoder


class TestArithmeticCoder(unittest.TestCase):

    INPUT_DATA = "a" * 3
    INPUT_DATA += "\n"

    COMPRESSED_DATA = "\x60\xff\x9b\xbf\x6c"

    def setUp(self):
        model = models.AdaptiveModel()
        self.ac = ArithmeticCoder(model)

    def test_coder(self):
        result = self.ac.encode(self.INPUT_DATA)
        self.assertEqual(result, self.COMPRESSED_DATA)

    def test_decoder(self):
        result = self.ac.decode(self.COMPRESSED_DATA)
        self.assertEqual(result, self.INPUT_DATA)

    def test_compress_decompress(self):
        test_data = "a" * 200
        test_data += "b" * 300
        test_data += "c" * 25
        compressed = self.ac.encode(test_data)
        decoder = ArithmeticCoder(models.AdaptiveModel())
        decompressed = decoder.decode(compressed)
        self.assertEqual(test_data, decompressed)



if __name__ == "__main__":
    unittest.main()
# eof
