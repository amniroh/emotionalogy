# -*- coding: utf-8 -*-

from twython import Twython  
import json
import hashlib
import logging
import sys



## Example command to run this:
## python tweets_new.py file_name verbose

# Instantiate an object
with open('creds.json') as f:
	creds = json.load(f)
#consumer_key = 'ksNYIZATik6GsTTAGlIDpfcZH'
#consumer_secret = '1kMEmM6oPnHnO87MablmdGTVI2Ji1JDIp0mE6KGanfNIgMWciW'
language = sys.argv[1]

python_tweets = Twython(creds['consumer_key'], creds['consumer_secret'])

# import pandas as pd
logging.basicConfig(
    filename="/home/ali/workspace/emotionalogy/status/status_" + language,
    level=logging.INFO,
    format="%(asctime)s:%(levelname)s:%(message)s"
    )


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
    path = '/home/ali/workspace/data/' + language + '/'  + emotion + '.json'
    try:
        with open(path, 'r') as f:
            past_data = json.load(f)
    except FileNotFoundError:
        past_data = {}
    data = results(emoji,lang=language)

    with open(path, 'w') as f:
        num_updates = len(data.keys() - past_data.keys())
        num_past = len(past_data)
        past_data.update(data)
        json.dump(past_data, f)
        logging.info(
            "{emotion} for {lang} before updates {past}, updated with {new}".format(
                emotion=emotion,
                past=num_past,
                new=num_updates,
                lang=language
            )
        )
#    if len(past_data) > 0 :
#        with open('datadiff/' + emotion, 'w') as f:
#            for text in (set(res['text']) - past_data):
#                f.write(text + '\n')
