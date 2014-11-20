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

num_to_train = 30
num_to_test = 30
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
    print 'Parsing review number: ',  count

  review_json = json.loads(raw_review)
  stars = review_json['stars']
  text = review_json['text'].lower()
  
  if count < num_to_train:
    features = build_feature_set(text)
    feature_set.append((features, stars))
  elif count < num_to_train + num_to_test:
    test_set.append((stars, text))
  else:
    break

end = datetime.now()
print 'Done parsing reviews json.'
print 'Completed in: ',  end - start
print 'Training naive bayes classifier on features.'

start = datetime.now()
unigram_nb = nltk.NaiveBayesClassifier.train(feature_set)
end = datetime.now()
print 'Finished training naive bayes classifier.'
print 'Completed in: ',  end - start


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
  predicted_stars = unigram_nb.classify(test_feature_set)
  counts[test_stars] += 1
  if test_stars == predicted_stars:
    tp[test_stars] += 1
  else:
    fn[test_stars] += 1
    fp[predicted_stars] += 1

print 'Finished analysis, printing results:'

for stars in xrange(1, 6):
  print 'Tested classifier on ',  counts[stars] , ' ',  stars , ' reviews'
  precision = 0.0
  if tp[stars] + fp[stars] == 0.0: 
    precision = tp[stars] / (tp[stars] + fp[stars])
  recall = 0.0
  if tp[stars] + fn[stars] == 0.0:
    recall = tp[stars] / (tp[stars] + fn[stars])
  print 'with precision: ',  precision
  print 'and recall:     ',  recall
  f1 = 0.0
  if not recall + precision == 0.0:
    f1 = 2 * precision * recall / (precision + recall)
  print 'and f1:         ',  f1



