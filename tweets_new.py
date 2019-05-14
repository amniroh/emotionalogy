# -*- coding: utf-8 -*-

from twython import Twython  
import json
import hashlib
import logging
# import pandas as pd
logging.basicConfig(
    filename="status",
    level=logging.INFO,
    format="%(asctime)s:%(levelname)s:%(message)s"
    )




## Example command to run this:
## python tweets_new.py file_name verbose

# Instantiate an object
consumer_key = 'YOUR_KEY'
consumer_secret = 'YOUR_SECRET'

python_tweets = Twython(consumer_key, consumer_secret)

# Create our query
limit = 100000
smileys = {
    'anger': '😡',
    'fear': '😨',
    'sad': '😞',
    'surprise': '😮',
    'happy': '😊',
    'tender': '😐',
    'excited': '😍',
    'disgust': '🤢',
}

def hash_func(
    user,
    date,
    text,
    favorite_count
):
    return hashlib.md5(
        '_'.join([
            user,
            date,
            text,
            favorite_count
        ]).encode()
    ).hexdigest()

def results(query, count=limit, lang='fa'):
    query = {'q': query, 
            'count': count,
            'lang': lang,
            }

    # Search tweets
    data = {}

    for status in python_tweets.search(**query)['statuses']:
        dict_info = {
			'user': status['user']['screen_name'],
			'date': status['created_at'],
			'text': status['text'],
			'favorite_count': str(status['favorite_count'])
        }
        key = hash_func(**dict_info)
        data[key] = dict_info
    return data


for emotion, emoji in smileys.items():
    try:
        with open('data/' + emotion + '.json', 'r') as f:
            past_data = json.load(f)
    except FileNotFoundError:
        past_data = {}
    data = results(emoji)

    with open('data/' + emotion + '.json', 'w') as f:
        num_updates = len(data.keys() - past_data.keys())
        num_past = len(past_data)
        past_data.update(data)
        json.dump(past_data, f)
        logging.info(
            "{emotion} before updates {past}, updated with {new}".format(
                emotion=emotion,
                past=num_past,
                new=num_updates
            )
        )
#    if len(past_data) > 0 :
#        with open('datadiff/' + emotion, 'w') as f:
#            for text in (set(res['text']) - past_data):
#                f.write(text + '\n')
