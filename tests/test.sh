#!/usr/bin/env bash

set -x # set debug

input_file=tests/pride_and_prejudice.txt
output_file=compressed
e_output_file=decompressed

exit_status=0
# use adaptive model
python main.py -i $input_file -o $output_file -a compression
python main.py -i $output_file -o $e_output_file -a decompression


diff $input_file $e_output_file
if [ $? -ne 0 ];
then
    echo "Error: adaptive model test failed"
    exit_status=1
fi

rm $output_file $e_output_file

# use simple static model
static_model=static_model
python main.py -i $input_file -o $output_file -a compression --output_model $static_model
python main.py -i $output_file -o $e_output_file -a decompression --input_model $static_model

diff $input_file $e_output_file
if [ $? -ne 0 ];
then
    echo "Error: static model test failed"
    exit_status=1
fi

rm $output_file $e_output_file $static_model

exit $exit_status

