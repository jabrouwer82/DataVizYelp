#! /bin/python3
import getopt
import json
import nltk
import operator
import os
import random
import sys

from datetime import datetime
from nltk.corpus import stopwords

num_training = 0
opts = getopt.getopt(sys.argv[1:], 'i:d:n:s:', ['input_dir=', 'dev='])
input_dir = './'
for opt, arg in opts[0]:
  if opt in ('-i', '--input_dir'):
    input_dir = arg
  elif opt in ('-d', '--dev'):
    num_training = int(arg)

word_counts = [{}, {}, {}, {}, {}, {}]

num_reviews = 1125458
update_freq = num_reviews / 30
count = 0
start = datetime.now()

feature_set = []
# Contents of the feature_set should be in the form ({feature_name: feature_val}, label)

print 'Parsing reviews json into frequency distributions.'
raw_reviews = open(os.path.join(input_dir, "yelp_academic_dataset_review.json"))
# Parses a review object
for raw_review in raw_reviews:
  count += 1
  if count % update_freq == 0:
    print 'Parsing review number:',  count

  review_json = json.loads(raw_review)
  stars = int(review_json['stars'])
  text = review_json['text'].lower()

  if num_training > 0: 
    if count < num_training:
      tokens = nltk.tokenize.word_tokenize(text)
      for token in tokens:
        word_counts[stars][token] = word_counts[stars].get(token, 0) + 1
    else:
      break
  else:
    tokens = nltk.tokenize.word_tokenize(text)
    for token in tokens:
      word_counts[stars][token] = word_counts[stars].get(token, 0) + 1
    

print 'There are', len(word_counts[1]), 'unique words in 1 star reviews'
print 'There are', len(word_counts[2]), 'unique words in 2 star reviews'
print 'There are', len(word_counts[3]), 'unique words in 3 star reviews'
print 'There are', len(word_counts[4]), 'unique words in 4 star reviews'
print 'There are', len(word_counts[5]), 'unique words in 5 star reviews'

