#! /bin/python3
import getopt
import json
import os
import nltk
import sys

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


feature_set = []
# Contents of the feature_set should be in the form ({feature_name: feature_val}, label)

print 'Parsing reviews json into frequency distributions.'
raw_reviews = open(os.path.join(input_dir, "yelp_academic_dataset_review.json"))
# Parses a review object
for raw_review in raw_reviews:
  review_json = json.loads(raw_review)
  stars = review_json['stars']
  text = review_json['text'].lower()

  features = build_feature_set(text)
  feature_set.append((features, stars))

print 'Done parsing reviews json.'
print 'Converting frequency distributions into probability distributions.'

unigram_nb = nltk.NaiveBayesClassifier.train(feature_set)
