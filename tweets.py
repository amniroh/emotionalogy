import time
import pycurl
import urllib.parse
import json
import oauth2 as oauth
import base64
import requests
import urllib.parse

OAUTH2_TOKEN = 'https://api.twitter.com/oauth2/token'
### twitter authorization doc
# https://developer.twitter.com/en/docs/basics/authentication/overview/oauth
 
API_ENDPOINT_URL = 'https://api.twitter.com/1.1/search/tweets.json?q=hi'
USER_AGENT = 'TwitterStream 1.0' # This can be anything really
 
# You need to replace these with your own values
consumer_key = ''
consumer_secret = ''
OAUTH_KEYS = {'consumer_key': consumer_key,
              'consumer_secret': consumer_secret,
              'access_token_key': '',
              'access_token_secret': ''}
 
# These values are posted when setting up the connection
POST_PARAMS = {'include_entities': 0,
               'stall_warning': 'true',
               'track': 'iphone,ipad,ipod'}
 
class TwitterStream:
    def __init__(self):
        self.oauth_token = oauth.Token(key=OAUTH_KEYS['access_token_key'], secret=OAUTH_KEYS['access_token_secret'])
        self.oauth_consumer = oauth.Consumer(key=OAUTH_KEYS['consumer_key'], secret=OAUTH_KEYS['consumer_secret'])
        self.conn = None
        self.tweets = []
        self.setup_connection()
 
    def setup_connection(self):
        """ Create persistant HTTP connection to Streaming API endpoint using cURL.
        """
        if self.conn:
            self.conn.close()
        self.conn = pycurl.Curl()
        self.conn.setopt(pycurl.HTTPGET, True)
        self.conn.setopt(pycurl.VERBOSE, True)
        self.conn.setopt(pycurl.URL, API_ENDPOINT_URL)
        self.conn.setopt(pycurl.USERAGENT, USER_AGENT)
        # Using gzip is optional but saves us bandwidth.
#        self.conn.setopt(pycurl.ENCODING, 'deflate, gzip')
#        self.conn.setopt(pycurl.POST, 1)
#        self.conn.setopt(pycurl.POSTFIELDS, urllib.urlencode(POST_PARAMS))
        self.conn.setopt(pycurl.HTTPHEADER, [
#            'Host: api.twitter.com',
            'authorization: %s' % self.get_oauth_header()
        ])
        # self.handle_tweet is the method that are called when new tweets arrive
        self.conn.setopt(pycurl.WRITEFUNCTION, self.handle_tweet)


    def get_oauth_header(self):
        """ Create and return OAuth header.
        """
        params = {'oauth_version': '1.0',
                  'oauth_nonce': oauth.generate_nonce(),
                  'oauth_timestamp': str(int(time.time()))}
        req = oauth.Request(method='GET', parameters=params, url='%s' % (API_ENDPOINT_URL))
#        token = self.get_bearer_token(consumer_key, consumer_secret)
        req.sign_request(oauth.SignatureMethod_HMAC_SHA1(), self.oauth_consumer, self.oauth_token)
        return req.to_header()['Authorization'].encode('utf-8')

    def run(self):
        self.conn.perform()

    def handle_tweet(self, data):
        """ This method is called when data is received through Streaming endpoint.
        """
        self.tweets.append(data)
#        if data.endswith('\r\n') and self.buffer.strip():
#            # complete message received
#            message = json.loads(self.buffer)
#            self.buffer = ''
#            msg = ''
#            if message.get('limit'):
#                print 'Rate limiting caused us to miss %s tweets' % (message['limit'].get('track'))
#            elif message.get('disconnect'):
#                raise Exception('Got disconnect: %s' % message['disconnect'].get('reason'))
#            elif message.get('warning'):
#                print 'Got warning: %s' % message['warning'].get('message')
#            else:
#                print 'Got tweet with text: %s' % message.get('text')

    def get_bearer_token(
        self,
        consumer_key=consumer_key,
        consumer_secret=consumer_secret
    ):
        # enconde consumer key
        consumer_key = urllib.parse.quote(consumer_key)
        # encode consumer secret
        consumer_secret = urllib.parse.quote(consumer_secret)
        # create bearer token
        bearer_token = consumer_key + ':' + consumer_secret
        # base64 encode the token
        base64_encoded_bearer_token = base64.b64encode(bearer_token.encode('utf-8'))
        # set headers
        headers = {
            "Authorization": "Basic " + base64_encoded_bearer_token.decode('utf-8') + "",
            "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
            "Content-Length": "29"}
    
        response = requests.post(OAUTH2_TOKEN, headers=headers, data={'grant_type': 'client_credentials'})
        to_json = response.json()
        return to_json['access_token']




obj = TwitterStream()
obj.run()
