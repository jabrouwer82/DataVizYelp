#! python3
import getopt
import itertools
import json
import math
import os
import sys

# Usage: python convert.py [(-i | --input_dir) <location of yelp json files>]
#                          [(-o | --output_dir) <location to put generated sql files>]
# Example: python convert.py -i ~/yelp/ -o ../bin/
# -i or --input_dir to specify the location of yelp json files (default ./)
# -o or --output_dir to specify where to put the generated sql insert file[s]
#   (default ../bin/

# CMD opts handling
opts = getopt.getopt(sys.argv[1:], 'i:o:', ['input_dir=', 'output_dir='])
input_dir = './'
output_dir = '../bin/'
for opt, arg in opts[0]:
  if opt in ('-i', '--input_dir'):
    input_dir = arg
  if opt in ('-o', '--output_dir'):
    output_dir = arg
input_dir = os.path.realpath(os.path.expanduser(input_dir))
output_dir = os.path.realpath(os.path.expanduser(output_dir))
raw_reviews = open(os.path.join(input_dir, "yelp_academic_dataset_review.json"))

print('Parsing review.json ...')
count = 0
# Parses a review object
for raw_review in raw_reviews:
  review_json = json.loads(raw_review)
  count += 1

print(count)
