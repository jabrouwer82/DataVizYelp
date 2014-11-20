#! /bin/python3
import getopt
import json
import os
import nltk
import sys
from datetime import datetime

opts = getopt.getopt(sys.argv[1:], 'i:o:', ['input_dir=', 'output_dir='])
input_dir = './'
output_dir = '../bin/'
for opt, arg in opts[0]:
  if opt in ('-i', '--input_dir'):
    input_dir = arg
  if opt in ('-o', '--output_dir'):
    output_dir = arg

def build_feature_set(text):
  tokens = nltk.tokenize.word_tokenize(text)
  features = {}
  for token in tokens:
    features[token] = features.get(token, 0) + 1
#    unigrams_cond_freq[stars][token] += 1
#    unigrams_freq[token] += 1

#  tokens_bigrams = nltk.bigrams(tokens)

#  for token in tokens_bigrams:
#    features[token] += 1
#    bigrams_cond_freq[stars][token] += 1
#    bigrams_freq[token] += 1

#  tokens_trigrams = nltk.bigrams(tokens)

#  for token in tokens_trigrams:
#    trigrams_cond_freq[stars][token] += 1
#    bigrams_freq[token] += 1
  return features

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

  if count % update_freq == 0:
    print 'Parsing review number: ' + count

  review_json = json.loads(raw_review)
  stars = review_json['stars']
  text = review_json['text'].lower()

  features = build_feature_set(text)
  feature_set.append((features, stars))

end = datetime.now()
print 'Done parsing reviews json.'
print 'Completed in: ' end - start
print 'Training naive bayes classifier on features.'

start = datetime.now()
unigram_nb = nltk.NaiveBayesClassifier.train(feature_set)
end = datetime.now()
print 'Finished training naive bayes classifier.'
print 'Completed in: ' end - start

