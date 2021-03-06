#! python3
import getopt
import itertools
import json
import math
import os
import sys

# Usage: python convert.py [(-i | --input_dir) <location of yelp json files>]
#                          [(-o | --output_dir) <location to put generated sql files>]
# Example: python convert.py -i ~/yelp/ -o ../bin/
# -i or --input_dir to specify the location of yelp json files (default ./)
# -o or --output_dir to specify where to put the generated sql insert file[s]
#   (default ../bin/

# CMD opts handling
opts = getopt.getopt(sys.argv[1:], 'i:o:', ['input_dir=', 'output_dir='])
input_dir = './'
output_dir = '../bin/'
for opt, arg in opts[0]:
  if opt in ('-i', '--input_dir'):
    input_dir = arg
  if opt in ('-o', '--output_dir'):
    output_dir = arg
input_dir = os.path.realpath(os.path.expanduser(input_dir))
output_dir = os.path.realpath(os.path.expanduser(output_dir))
raw_businesses = open(os.path.join(input_dir, "yelp_academic_dataset_business.json"))
raw_users = open(os.path.join(input_dir, "yelp_academic_dataset_user.json"))
raw_checkins = open(os.path.join(input_dir, "yelp_academic_dataset_checkin.json"))
raw_reviews = open(os.path.join(input_dir, "yelp_academic_dataset_review.json"))
# raw_tips = open(os.path.join(input_dir, "yelp_academic_dataset_tip.json"))

# The following 2 dicts and sets conatain all relevant objects mapped by their
# given yelp ids. After that are 11 lists that contain the objects which were
# not given ids by yelp. Should be a 1-1 relation with the sql tables. Following
# each map/list is the generator that is used to create each primary key.

attribute_gen = itertools.count(0,1)
attributes = {}
business_gen = itertools.count(0,1)
businesses = {}
categories = {}
category_gen = itertools.count(0,1)
elite_year_gen = itertools.count(0,1)
elite_years = {}
neighborhood_gen = itertools.count(0,1)
neighborhoods = {}
user_gen = itertools.count(0,1)
users = {}

checkin_gen = itertools.count(0,1)
checkin_info_gen = itertools.count(0,1)
checkin_infos = []
checkins = []
compliment_gen = itertools.count(0,1)
compliments = []
hours = []
hours_gen = itertools.count(0,1)
review_gen = itertools.count(0,1)
reviews = []
vote_gen = itertools.count(0,1)
votes = []

# The folowing 7 lists are the lists of pairs that fill the many to many
# relation tables. Should be a 1-1 with the sql relation tables
business_neighborhoods = []
attribute_businesses = []
review_votes = []
user_votes = []
elite_year_users = []
business_categories = []
user_friends = []
relation_tables = set(['attribute_business', 'business_neighborhood', 'elite_year_yelper', 'business_category', 'yelper_friend'])

print('Parsing business.json ...', end='')
sys.stdout.flush()
business_count = 0
# Parses a business object
for raw_business in raw_businesses:
  business_json = json.loads(raw_business)
  business = {}
  business_pk = business_gen.__next__()
  business['business_id'] = business_pk
  business['business_id_str'] = business_json['business_id']
  business['business_name'] = business_json['name']
  business['address'] = business_json['full_address']
  business['city'] = business_json['city']
  business['state'] = business_json['state']
  business['latitude'] = business_json['latitude']
  business['longitude'] = business_json['longitude']
  business['stars'] = business_json['stars']
  business['review_count'] = business_json['review_count']
  business['business_open'] = 1 if business_json['open'] else 0
  businesses[business_json['business_id']] = business

# Parses an attribute object
  attributes_json = business_json['attributes']
  for attribute_name, attribute_value in attributes_json.items():
    if isinstance(attribute_value, dict):
      for sub_attribute_name, sub_attribute_value in attribute_value.items():
        assert not isinstance(sub_attribute_value, dict)
        attribute = (attribute_name + ' ' + sub_attribute_name,
                     1 if sub_attribute_value else 0)
        attribute_pk = 0
        if not attribute in attributes:
          attribute_pk = attribute_gen.__next__()
          attributes[attribute] = attribute_pk
        else:
          attribute_pk = attributes[attribute]
        attribute_businesses.append((attribute_pk, business_pk))
    else:
      attribute = (attribute_name,
                   1 if attribute_value else 0)
      attribute_pk = 0
      if not attribute in attributes:
        attribute_pk = attribute_gen.__next__()
        attributes[attribute] = attribute_pk
      else:
        attribute_pk = attributes[attribute]
      attribute_businesses.append((attribute_pk, business_pk))

# Parses a neighborhood object
  neighborhood_list = business_json['neighborhoods']
  for neighborhood in neighborhood_list:
    if not neighborhood in neighborhoods:
      neighborhood_pk = neighborhood_gen.__next__()
      neighborhoods[neighborhood] = neighborhood_pk
    else:
      neighborhood_pk = neighborhoods[neighborhood]
    business_neighborhoods.append((business_pk, neighborhood_pk))
  
# Parses a category object
  category_list = business_json['categories']
  for category in category_list:
    if not category in categories:
      category_pk = category_gen.__next__()
      categories[category] = category_pk
    else:
      category_pk = categories[category]
    business_categories.append((business_pk, category_pk))

# Parses an hour object
  hours_list = business_json['hours']
  for day, open_closes in hours_list.items():
    for open_close, time in open_closes.items():
      hour = {}
      hour_pk = hours_gen.__next__()
      hour['hours_id'] = hour_pk
      hour['hours_day'] = day
      hour['hours_open'] = open_close
      hour['hours_time'] = time
      hour['business_id'] = business_pk
      hours.append(hour)

print(' done')
print('Parsing user.json ...', end='')
sys.stdout.flush()
# Parses a user/yelper object
for raw_user in raw_users:
  user_json = json.loads(raw_user)
  user = {}
  user_pk = user_gen.__next__()
  user['yelper_id'] = user_pk
  user['yelper_id_str'] = user_json['user_id']
  user['yelper_name'] = user_json['name']
  user['review_count'] = user_json['review_count']
  user['yelping_since'] = user_json['yelping_since']
  user['average_stars'] = user_json['average_stars']
  user['fans'] = user_json['fans']
  user['friends'] = user_json['friends']
  users[user['yelper_id_str']] = user

# Parses a vote object
  for vote_type, vote_count in user_json['votes'].items():
    vote = {}
    vote_pk = vote_gen.__next__()
    vote['vote_id'] = vote_pk
    vote['vote_type'] = vote_type
    vote['vote_count'] = vote_count
    vote['yelper_id'] = user_pk
    votes.append(vote)

# Parses an elite_year object
  for elite_year in user_json['elite']:
    if elite_year in elite_years:
      elite_year_pk = elite_years[elite_year]
    else:
      elite_year_pk = elite_year_gen.__next__()
      elite_years[elite_year] = elite_year_pk
    elite_year_users.append((elite_year_pk, user_pk))

# Parses a compliment
  for compliment_type, compliment_count in user_json['compliments'].items():
    compliment = {}
    compliment['compliment_id'] = compliment_gen.__next__()
    compliment['compliment_type'] = compliment_type
    compliment['compliment_count'] = compliment_count
    compliment['yelper_id'] = user_pk
    compliments.append(compliment)

print(' done')
print('Calculating friends ...', end='')
sys.stdout.flush()
# Parses the list of friends
for user_pk, user in users.items():
  for friend_id in user['friends']:
    friend = users[friend_id]
    user_friends.append((user['yelper_id'], friend['yelper_id']))

print(' done')
print('Parsing review.json ...', end='')
sys.stdout.flush()
# Parses a review object
for raw_review in raw_reviews:
  review_json = json.loads(raw_review)
  review = {}
  review_pk = review_gen.__next__()
  review['review_id'] = review_pk
  review['business_id'] = businesses[review_json['business_id']]['business_id']
  review['yelper_id'] = users[review_json['user_id']]['yelper_id']
  review['stars'] = review_json['stars']
  review['text'] = review_json['text']
  review['review_date'] = review_json['date']
  reviews.append(review)
  
# Parses a vote object
  for vote_type, vote_count in review_json['votes'].items():
    vote = {}
    vote_pk = vote_gen.__next__()
    vote['vote_id'] = vote_pk
    vote['vote_type'] = vote_type
    vote['vote_count'] = vote_count
    vote['yelper_id'] = review_pk
    votes.append(vote)

print(' done')
print('Parsing checkin.json ...', end='')
sys.stdout.flush()
# Parses a checkin object
for raw_checkin in raw_checkins:
  checkin_json = json.loads(raw_checkin)
  checkin = {}
  checkin_pk = checkin_gen.__next__()
  checkin['checkin_id'] = checkin_pk
  checkin['business_id'] = businesses[checkin_json['business_id']]['business_id']
  checkins.append(checkin)

  for checkin_time, checkin_count in checkin_json['checkin_info'].items():
    checkin_info = {}
    checkin_info_pk = checkin_info_gen.__next__()
    checkin_info['checkin_info_id'] = checkin_info_pk
    checkin_info['checkin_time'] = checkin_time
    checkin_info['checkin_count'] = checkin_count
    checkin_info['checkin_id'] = checkin_pk
    checkin_infos.append(checkin_info)

print(' done')

INSERT = 'INSERT INTO '
BUSINESS_INSERT = INSERT + 'business (business_id, business_id_str, business_name, address, city, state, latitude, longitude, stars, review_count, business_open) VALUES ({}, q\'#{}#\', q\'#{}#\', q\'#{}#\', q\'#{}#\', q\'#{}#\', {}, {}, {}, {}, q\'#{}#\');\n'
ATTRIBUTE_INSERT = INSERT + 'attribute (attribute_id, attribute_name, attribute_value) VALUES ({}, q\'#{}#\', q\'#{}#\');\n'
RELATION_INSERT = INSERT + '{} ({}, {}) VALUES ({}, {});\n'
NEIGHBORHOOD_INSERT = INSERT + 'neighborhood (neighborhood_id, neighborhood_name) VALUES ({}, q\'#{}#\');\n'
CATEGORY_INSERT = INSERT + 'category (category_id, category_name) VALUES ({}, q\'#{}#\');\n'
HOURS_INSERT = INSERT + 'hours (hours_id, hours_day, hours_open, hours_time, business_id) VALUES ({}, q\'#{}#\', q\'#{}#\', q\'#{}#\', {});\n'
USER_INSERT = INSERT + 'yelper (yelper_id, yelper_id_str, yelper_name, review_count, average_stars, yelping_since, fans) VALUES ({}, q\'#{}#\', q\'#{}#\', {}, {}, to_date(\'{}\', \'YYYY-MM\'), {});\n'
VOTE_INSERT = INSERT + 'vote (vote_id, vote_type, vote_count, yelper_id, review_id) VALUES ({}, q\'#{}#\', {}, {}, {});\n'
ELITE_YEAR_INSERT = INSERT + 'elite_year (elite_year_id, elite_year) VALUES ({}, q\'#{}#\');\n'
COMPLIMENT_INSERT = INSERT + 'compliment (compliment_id, compliment_type, compliment_count, yelper_id) VALUES ({}, q\'#{}#\', {}, {});\n'
REVIEW_INSERT = INSERT + 'review (review_id, business_id, yelper_id, stars, text, review_date) VALUES ({}, {}, {}, {}, q\'#{}#\', to_date(\'{}\', \'YYYY-MM-DD\'));\n'
CHECKIN_INSERT = INSERT + 'checkin (checkin_id, business_id) VALUES ({}, {});\n'
CHECKIN_INFO_INSERT = INSERT + 'checkin_info (checkin_info_id, checkin_time, checkin_count, checkin_id) VALUES ({}, q\'#{}#\', {}, {});\n'
def insert_format(table, values):
  if table == 'business':
    return BUSINESS_INSERT.format(values['business_id'],
                                  values['business_id_str'],
                                  values['business_name'],
                                  values['address'],
                                  values['city'],
                                  values['state'],
                                  values['latitude'],
                                  values['longitude'],
                                  values['stars'],
                                  values['review_count'],
                                  values['business_open'])
  if table == 'attribute':
    return ATTRIBUTE_INSERT.format(values['attribute_id'],
                                   values['attribute_name'],
                                   values['attribute_value'])
  if table in relation_tables:
    return RELATION_INSERT.format(table,
                                  values[0],
                                  values[1],
                                  values[2],
                                  values[3])
  if table == 'neighborhood':
    return NEIGHBORHOOD_INSERT.format(values[0],
                                      values[1])
  if table == 'category':
    return CATEGORY_INSERT.format(values[0],
                                  values[1])
  if table == 'hours':
    return HOURS_INSERT.format(values['hours_id'],
                               values['hours_day'],
                               values['hours_open'],
                               values['hours_time'],
                               values['business_id'])
  if table == 'user':
    return USER_INSERT.format(values['yelper_id'],
                              values['yelper_id_str'],
                              values['yelper_name'],
                              values['review_count'],
                              values['average_stars'],
                              values['yelping_since'],
                              values['fans'])
  if table == 'vote':
    return VOTE_INSERT.format(values['vote_id'],
                              values['vote_type'],
                              values['vote_count'],
                              values.get('yelper_id', 'NULL'),
                              values.get('review_id', 'NULL'))
  if table == 'elite_year':
    return ELITE_YEAR_INSERT.format(values[0],
                             values[1])
  if table == 'compliment':
    return COMPLIMENT_INSERT.format(values['compliment_id'],
                                    values['compliment_type'],
                                    values['compliment_count'],
                                    values['yelper_id'])
  if table == 'review':
    return REVIEW_INSERT.format(values['review_id'],
                                values['business_id'],
                                values['yelper_id'],
                                values['stars'],
                                values['text'],
                                values['review_date'])
  if table == 'checkin':
    return CHECKIN_INSERT.format(values['checkin_id'],
                                 values['business_id'])
  if table == 'checkin_info':
    return CHECKIN_INFO_INSERT.format(values['checkin_info_id'],
                                      values['checkin_time'],
                                      values['checkin_count'],
                                      values['checkin_id'])

def output_file_duration(size, count):
  count += 1
  if count in [math.floor(.1 * x * size) for x in range(1, 11)]:
    print('=', end='')
    sys.stdout.flush()
  return count

def new_file(name):
  # This is foul, but it's not worth the time to do it right.
  print('Generating {:<26}'.format(name + '.dml') + ' [', end='')
  sys.stdout.flush()
  # Business json output dml file
  new_output_file = open(os.path.join(output_dir, name + '.dml'), 'w')
  new_output_file.write('set define off\n')
  new_output_file.write('set termout off\n')
  new_output_file.write('set echo off\n')
  return new_output_file

def close_file(old_output_file):
  old_output_file.close()
  print('] done')

output_file_size = len(businesses)
output_file_count = 0
output_file = new_file('business')
for business_id, business in businesses.items():
  insert = insert_format('business', business)
  output_file.write(insert)

  output_file_count = output_file_duration(output_file_size, output_file_count)

close_file(output_file)
output_file_size = len(attributes)
output_file_count = 0
output_file = new_file('attribute')
for attribute, attribute_pk in attributes.items():
  final_attribute = {}
  final_attribute['attribute_name'] = attribute[0]
  final_attribute['attribute_value'] = 1 if attribute[1] else 0
  final_attribute['attribute_id'] = attribute_pk
  insert = insert_format('attribute', final_attribute)
  output_file.write(insert)

  output_file_count = output_file_duration(output_file_size, output_file_count)

close_file(output_file)
output_file_size = len(attribute_businesses)
output_file_count = 0
output_file = new_file('attribute_business')
for attribute_business in attribute_businesses:
  attribute_business = ('attribute_id', 'business_id') + attribute_business
  insert = insert_format('attribute_business', attribute_business)
  output_file.write(insert)

  output_file_count = output_file_duration(output_file_size, output_file_count)

close_file(output_file)
output_file_size = len(neighborhoods)
output_file_count = 0
output_file = new_file('neighborhood')
for neighborhood, neighborhood_pk in neighborhoods.items():
  insert = insert_format('neighborhood', (neighborhood_pk, neighborhood))
  output_file.write(insert)

  output_file_count = output_file_duration(output_file_size, output_file_count)

close_file(output_file)
output_file_size = len(business_neighborhoods)
output_file_count = 0
output_file = new_file('business_neighborhood')
for business_neighborhood in business_neighborhoods:
  business_neighborhood = ('business_id', 'neighborhood_id') + business_neighborhood
  insert = insert_format('business_neighborhood', business_neighborhood)
  output_file.write(insert)

  output_file_count = output_file_duration(output_file_size, output_file_count)

close_file(output_file)
output_file_size = len(categories)
output_file_count = 0
output_file = new_file('category')
for category, category_pk in categories.items():
  insert = insert_format('category', (category_pk, category))
  output_file.write(insert)

  output_file_count = output_file_duration(output_file_size, output_file_count)

close_file(output_file)
output_file_size = len(business_categories)
output_file_count = 0
output_file = new_file('business_category')
for business_category in business_categories:
  business_category = ('business_id', 'category_id') + business_category
  insert = insert_format('business_category', business_category)
  output_file.write(insert)

  output_file_count = output_file_duration(output_file_size, output_file_count)

close_file(output_file)
output_file_size = len(hours)
output_file_count = 0
output_file = new_file('hour')
for hour in hours:
  insert = insert_format('hours', hour)
  output_file.write(insert)

  output_file_count = output_file_duration(output_file_size, output_file_count)

close_file(output_file)
output_file_size = len(users)
output_file_count = 0
output_file = new_file('user')
for user in users.values():
  insert = insert_format('user', user)
  output_file.write(insert)

  output_file_count = output_file_duration(output_file_size, output_file_count)

close_file(output_file)
output_file_size = len(votes)
output_file_count = 0
output_file = new_file('vote')
for vote in votes:
  insert = insert_format('vote', vote)
  output_file.write(insert)

  output_file_count = output_file_duration(output_file_size, output_file_count)

close_file(output_file)
output_file_size = len(elite_years)
output_file_count = 0
output_file = new_file('elite_year')
for elite_year, elite_year_pk in elite_years.items():
  insert = insert_format('elite_year', (elite_year_pk, elite_year))
  output_file.write(insert)

  output_file_count = output_file_duration(output_file_size, output_file_count)

close_file(output_file)
output_file_size = len(elite_year_users)
output_file_count = 0
output_file = new_file('elite_year_user')
for elite_year_user in elite_year_users:
  elite_year_user = ('elite_year_id', 'yelper_id') + elite_year_user
  insert = insert_format('elite_year_yelper', elite_year_user)
  output_file.write(insert)

  output_file_count = output_file_duration(output_file_size, output_file_count)

close_file(output_file)
output_file_size = len(compliments)
output_file_count = 0
output_file = new_file('compliment')
for compliment in compliments:
  insert = insert_format('compliment', compliment)
  output_file.write(insert)

  output_file_count = output_file_duration(output_file_size, output_file_count)

close_file(output_file)
output_file_size = len(user_friends)
output_file_count = 0
output_file = new_file('user_friend')
for user_friend in user_friends:
  user_friend = ('yelper_id', 'friend_id') + user_friend
  insert = insert_format('yelper_friend', user_friend)
  output_file.write(insert)

  output_file_count = output_file_duration(output_file_size, output_file_count)

close_file(output_file)
output_file_size = len(reviews)
output_file_count = 0
output_file = new_file('review')
for review in reviews:
  insert = insert_format('review', review)
  output_file.write(insert)

  output_file_count = output_file_duration(output_file_size, output_file_count)

close_file(output_file)
output_file_size = len(checkins)
output_file_count = 0
output_file = new_file('checkin')
for checkin in checkins:
  insert = insert_format('checkin', checkin)
  output_file.write(insert)
  
  output_file_count = output_file_duration(output_file_size, output_file_count)

close_file(output_file)
output_file_size = len(checkin_infos)
output_file_count = 0
output_file = new_file('checkin_info')
for checkin_info in checkin_infos:
  insert = insert_format('checkin_info', checkin_info)
  output_file.write(insert)
  
  output_file_count = output_file_duration(output_file_size, output_file_count)

close_file(output_file)

print('{:>9,} businesses'.format(len(businesses)))
print('{:>9,} attributes'.format(len(attributes)))
print('{:>9,} attribute_businesses'.format(len(attribute_businesses)))
print('{:>9,} neighborhoods'.format(len(neighborhoods)))
print('{:>9,} business_neighborhoods'.format(len(business_neighborhoods)))
print('{:>9,} categories'.format(len(categories)))
print('{:>9,} business_categories'.format(len(business_categories)))
print('{:>9,} hours'.format(len(hours)))
print('{:>9,} users'.format(len(users)))
print('{:>9,} votes'.format(len(votes)))
print('{:>9,} elite_years'.format(len(elite_years)))
print('{:>9,} elite_year_users'.format(len(elite_year_users)))
print('{:>9,} compliments'.format(len(compliments)))
print('{:>9,} user_friends'.format(len(user_friends)))
print('{:>9,} reviews'.format(len(reviews)))
print('{:>9,} checkins'.format(len(checkins)))
print('{:>9,} checkin_infos'.format(len(checkin_infos)))

print('{:,} total entries'.format(len(businesses) + len(attributes) + len(attribute_businesses) + len(business_neighborhoods) + len(business_categories) + len(hours) + len(users) + len(votes) + len(elite_years) + len(elite_year_users) + len(compliments) + len(user_friends) + len(reviews) + len(checkins) + len(checkin_infos)))

