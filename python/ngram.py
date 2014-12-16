#! /bin/python3
import getopt
import json
import nltk
import operator
import os
import random
import sys

from nltk.probability import LidstoneProbDist
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

models = [[]]
words = [[], [], [], [], [], []]

num_reviews = 1125458
update_freq = num_reviews / 30
count = 0
start = datetime.now()

def generate(stars, n):
  

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
      words[stars].apend(tokens)
    else:
      break
  else:
    tokens = nltk.tokenize.word_tokenize(text)
    words[stars].apend(tokens)
    
print 'Training ngram models'
for x in xrange(1, 6):
  est = lambda fdist, bins: LidstoneProbDist(fdist, 0.2)
  models[x].append(NgramModel(3, words[x], estimator=est))




