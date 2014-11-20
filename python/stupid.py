# Shows precision, recall and f1 for classifier that randomly selects stars
import random

test_set = [random.randint(1, 5) for x in xrange(1000000)]

# Count of stars in the test data
counts = {5: 0.0, 4: 0.0, 3: 0.0, 2: 0.0, 1: 0.0}
# True positives, tp[x] = count of times real_stars == x == expected_stars
tp = {5: 0.0, 4: 0.0, 3: 0.0, 2: 0.0, 1: 0.0}
# False positives, fp[x] = count of times real_stars != x == expected_stars
fp = {5: 0.0, 4: 0.0, 3: 0.0, 2: 0.0, 1: 0.0}
# False negatives, fn[x] = count of times real_stars == x != expected_stars
fn = {5: 0.0, 4: 0.0, 3: 0.0, 2: 0.0, 1: 0.0}

for test_stars in test_set:
  predicted_stars = random.randint(1, 5)
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
  if not tp[stars] + fp[stars] == 0.0:
    precision = tp[stars] / (tp[stars] + fp[stars])
  recall = 0.0
  if not tp[stars] + fn[stars] == 0.0:
    recall = tp[stars] / (tp[stars] + fn[stars])
  print 'with precision: ',  precision
  print 'and recall:     ',  recall
  f1 = 0.0
  if not recall + precision == 0.0:
    f1 = 2 * precision * recall / (precision + recall)
  print 'and f1:         ',  f1
