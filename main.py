#!/usr/bin/env python

__author__ = 'Tomas Novacik'

# implementation is based on
# http://marknelson.us/2014/10/19/data-compression-with-arithmetic-coding/
# and c++ source
# http://marknelson.us/attachments/2014/ari/ari.zip

import argparse

import models

from arithmetic_coder import ArithmeticCoder


COMPRESSION = "compression"
DECOMPRESSION = "decompression"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input_file",
                        help="input file used for [de]compression",
                        required=True)
    parser.add_argument("-o", "--output_file",
                        help="output file used for [de]compression",
                        required=True)
    hlp_msg = "Action that should be executed on the input file."
    parser.add_argument("-a", "--action",
                        help=hlp_msg,
                        choices=[DECOMPRESSION, COMPRESSION],
                        required=True)

    parser.add_argument("--input_model",
                        help="Filename of the input model")

    parser.add_argument("--output_model",
                        help="Filename of the output model")

    args = parser.parse_args()

    with open(args.input_file) as ifile:
        input_data = ifile.read()
        if args.input_model:
            model = models.SimpleModel()
            model.load_from_file(args.input_model)
        elif args.output_model:
            model = models.SimpleModel(input_data)
        else:
            model = models.AdaptiveModel()

        ac = ArithmeticCoder(model)
        if args.action == COMPRESSION:
            output_data = ac.encode(input_data)
        else:
            output_data = ac.decode(input_data)

        with open(args.output_file, "w") as ofile:
            ofile.write(output_data)

        if args.output_model:
            model.save_to_file(args.output_model)

if __name__ == "__main__":
    main()

# eof
