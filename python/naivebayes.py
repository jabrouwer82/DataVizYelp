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


unigrams_cond_freq = nltk.ConditionalFreqDist()
unigrams_freq = nltk.FreqDist()
bigrams_cond_freq = nltk.ConditionalFreqDist()
bigrams_freq = nltk.FreqDist()
trigrams_cond_freq = nltk.ConditionalFreqDist()
trigrams_freq = nltk.FreqDist()


raw_reviews = open(os.path.join(input_dir, "yelp_academic_dataset_review.json"))
# Parses a review object
for raw_review in raw_reviews:
  review_json = json.loads(raw_review)
  stars = review_json['stars']
  text = review_json['text'].lower()
  
  tokens = nltk.tokenize.word_tokenize(text)

  for token in tokens:
    unigrams_cond_freq[stars][token] += 1
    unigrams_freq[token] += 1

  tokens_bigrams = nltk.bigrams(tokens)

  for token in tokens_bigrams:
    bigrams_cond_freq[stars][token] += 1
    bigrams_freq[token] += 1

  tokens_trigrams = nltk.bigrams(tokens)

  for token in tokens_trigrams:
    trigrams_cond_freq[stars][token] += 1
    bigrams_freq[token] += 1

unigrams_cond_prob = nltk.ConditionalProbDist(unigrams_cond_freq, nltk.LaplaceProbDist)
bigrams_cond_prob = nltk.ConditionalProbDist(bigrams_cond_freq, nltk.LaplaceProbDist)
trigrams_cond_prob = nltk.ConditionalProbDist(trigrams_cond_freq, nltk.LapaceProbDist)












