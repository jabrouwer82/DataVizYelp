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


#unigrams_cond_freq = nltk.ConditionalFreqDist()
#unigrams_freq = nltk.FreqDist()
#bigrams_cond_freq = nltk.ConditionalFreqDist()
#bigrams_freq = nltk.FreqDist()
#trigrams_cond_freq = nltk.ConditionalFreqDist()
#trigrams_freq = nltk.FreqDist()
#stars_freq = nltk.FreqDist()
5_feature_set = set()
4_feature_set = set()
3_feature_set = set()
2_feature_set = set()
1_feature_set = set()

print 'Parsing reviews json into frequency distributions.'
raw_reviews = open(os.path.join(input_dir, "yelp_academic_dataset_review.json"))
# Parses a review object
for raw_review in raw_reviews:
  review_json = json.loads(raw_review)
  stars = review_json['stars']
  text = review_json['text'].lower()
  feature_set = set()

  if (stars == 1) {
    feature_set = 1_feature_set
  } elif (stars == 2) {
    feature_set = 2_feature_set
  } elif (stars == 3) {
    feature_set = 3_feature_set
  } elif (stars == 4) {
    feature_set = 4_feature_set
  } elif (stars == 5) {
    feature_set = 5_feature_set
  } else {
    print 'Something went wrong'
    break
  }

#  stars_freq[stars] += 1

  tokens = nltk.tokenize.word_tokenize(text)

  for token in tokens:
    feature_set.add({'unigram': token}
#    unigrams_cond_freq[stars][token] += 1
#    unigrams_freq[token] += 1

  tokens_bigrams = nltk.bigrams(tokens)

  for token in tokens_bigrams:
    feature_set.add({'bigram': token})
#    bigrams_cond_freq[stars][token] += 1
#    bigrams_freq[token] += 1

#  tokens_trigrams = nltk.bigrams(tokens)

#  for token in tokens_trigrams:
#    trigrams_cond_freq[stars][token] += 1
#    bigrams_freq[token] += 1

print 'Done parsing reviews json.'
print 'Converting frequency distributions into probability distributions.'

#unigrams_cond_prob = nltk.ConditionalProbDist(unigrams_cond_freq, nltk.LaplaceProbDist)
#bigrams_cond_prob = nltk.ConditionalProbDist(bigrams_cond_freq, nltk.LaplaceProbDist)
#trigrams_cond_prob = nltk.ConditionalProbDist(trigrams_cond_freq, nltk.LapaceProbDist)

#unigrams_prob = nltk.LaplaceProbDist(unigrams_freq)
#bigrams_prob = nltk.LaplaceProbDist(bigrams_freq)
#trigrams_prob = nltk.LaplaceProbDist(trigrams_freq)

#stars_prob = nltk.MLEProbDist(stars_freq)

unigram_nb = nltk.NaiveBayesClassifier.train([(1_feature_set, 1), (2_feature_set, 2), (3_feature_set, 3), (4_feature_set, 4), (5_feature_set, 5)]








