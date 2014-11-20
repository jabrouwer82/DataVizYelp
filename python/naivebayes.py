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

opts = getopt.getopt(sys.argv[1:], 'i:d:n:s:', ['input_dir=', 'dev=', 'ngrams=', 'stopwords='])
input_dir = './'
num_training = 0
ngrams = '1'
stopword = 'none'
for opt, arg in opts[0]:
  if opt in ('-i', '--input_dir'):
    input_dir = arg
  elif opt in ('-d', '--dev'):
    num_training = int(arg)
  elif opt in ('-n', '--ngrams'):
    ngrams = arg
  elif opt in ('-s', '--stopwords'):
    stopword = arg


words_removed = 0
stopwords_list = []

if stopword != 'none':
  stopwords_list = stopwords.words('english')

def build_feature_set(text):
  tokens = nltk.tokenize.word_tokenize(text.lower())
  features = {}
  global words_removed
# unigrams
  if '1' in ngrams:
    for token in tokens:
      if not token in stopwords.words('english'):
        features[token] = features.get(token, 0) + 1
      else:
        words_removed += 1
  
#bigrams
  if '2' in ngrams:
    tokens_bigrams = nltk.bigrams(tokens)

    for token in tokens_bigrams:
      features[token] = features.get(token, 0) + 1

#trigrams
  if '3' in ngrams:
    tokens_trigrams = nltk.trigrams(tokens)

    for token in tokens_trigrams:
      features[token] = features.get(token, 0) + 1
  
  return features

test_set = []

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
  stars = review_json['stars']
  text = review_json['text'].lower()

  if num_training > 0: 
    if count < num_training:
      features = build_feature_set(text)
      feature_set.append((features, stars))
    elif count < 2 * num_training:
      test_set.append((stars, text))
    else:
      break
  else:
    # Sample 50% of data to be for training and 50% to be for testing
    if random.random() < 0.5:
      features = build_feature_set(text)
      feature_set.append((features, stars))
    else:
      test_set.append((stars, text))

end = datetime.now()
print 'Done parsing reviews json.'
print 'Completed in:',  end - start
print 'Selected', count - len(test_set), 'reviews for training.'
print 'Selected', len(test_set), 'reviews for testing.'
print 'Removed', words_removed, 'stopwords.'
print 'Training naive bayes classifier on features.'

start = datetime.now()
nb = nltk.NaiveBayesClassifier.train(feature_set)
end = datetime.now()
print 'Finished training naive bayes classifier.'
print 'Completed in:',  end - start


print 'Beginning analysis.'

# Count of stars in the test data
counts = {5: 0.0, 4: 0.0, 3: 0.0, 2: 0.0, 1: 0.0}
# True positives, tp[x] = count of times real_stars == x == expected_stars
tp = {5: 0.0, 4: 0.0, 3: 0.0, 2: 0.0, 1: 0.0}
# False positives, fp[x] = count of times real_stars != x == expected_stars
fp = {5: 0.0, 4: 0.0, 3: 0.0, 2: 0.0, 1: 0.0}
# False negatives, fn[x] = count of times real_stars == x != expected_stars
fn = {5: 0.0, 4: 0.0, 3: 0.0, 2: 0.0, 1: 0.0}

for test_stars, test_text in test_set:
  test_feature_set = build_feature_set(test_text)
  predicted_stars = nb.classify(test_feature_set)
  counts[test_stars] += 1
  if test_stars == predicted_stars:
    tp[test_stars] += 1
  else:
    fn[test_stars] += 1
    fp[predicted_stars] += 1

print 'Finished analysis, printing results:'

for stars in xrange(1, 6):
  print 'Tested classifier on',  counts[stars] ,  stars , 'star reviews'
  precision = 0.0
  if not tp[stars] + fp[stars] == 0.0: 
    precision = tp[stars] / (tp[stars] + fp[stars])
  recall = 0.0
  if not tp[stars] + fn[stars] == 0.0:
    recall = tp[stars] / (tp[stars] + fn[stars])
  print 'with precision:',  precision
  print 'and recall:    ',  recall
  f1 = 0.0
  if not recall + precision == 0.0:
    f1 = 2 * precision * recall / (precision + recall)
  print 'and f1:        ',  f1



