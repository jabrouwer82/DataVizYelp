# Shows precision, recall and f1 for classifier that randomly selects stars
import random

test_set = []

count_1 = 55336.0
count_2 = 51357.0
count_3 = 82098.0
count_4 = 171658.0
count_5 = 203193.0

total_count = int(count_1 + count_2 + count_3 + count_4 + count_5)

ratio_1 = 55336.0/total_count
ratio_2 = 51357.0/total_count
ratio_3 = 82098.0/total_count
ratio_4 = 171658.0/total_count
ratio_5 = 203193.0/total_count

def get_rand():
  rand = random.random()
  if (rand < ratio_1):
    return 1
  elif (rand < ratio_1 + ratio_2):
    return 2
  elif (rand < ratio_1 + ratio_2 + ratio_3):
    return 3
  elif (rand < ratio_1 + ratio_2 + ratio_3 + ratio_4):
    return 4
  elif (rand < ratio_1 + ratio_2 + ratio_3 + ratio_4 + ratio_5):
    return 5

for x in xrange(total_count):
  test_set.append(get_rand())

# Count of stars in the test data
counts = {5: 0.0, 4: 0.0, 3: 0.0, 2: 0.0, 1: 0.0}
# True positives, tp[x] = count of times real_stars == x == expected_stars
tp = {5: 0.0, 4: 0.0, 3: 0.0, 2: 0.0, 1: 0.0}
# False positives, fp[x] = count of times real_stars != x == expected_stars
fp = {5: 0.0, 4: 0.0, 3: 0.0, 2: 0.0, 1: 0.0}
# False negatives, fn[x] = count of times real_stars == x != expected_stars
fn = {5: 0.0, 4: 0.0, 3: 0.0, 2: 0.0, 1: 0.0}

for test_stars in test_set:
  #predicted_stars = get_rand()
  predicted_stars = random.randint(1,5)
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
