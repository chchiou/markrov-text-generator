import tweepy
import json
import re

import sqlite3
sql_conn = sqlite3.connect('tweets.db', isolation_level=None )
sql_cur = sql_conn.cursor()


# Authentication details. To  obtain these visit dev.twitter.com
consumer_key = 'IsLPAN0ECZUFgVpQ1hgDAeAHk'
consumer_secret = 'retGBqwK9CdGlzKovsTiDq5MCWGUnDEQ6thDVtCSFL1fDPcHc2'
access_token = '356253611-JZaxzUvLSUzQTnVaO2YTsgFvFuVAMXB46ONQwPna'
access_token_secret = 'Qko54nhzdQinOd3MZNAgJMM7sqlIy0oWU9f6f5EQPDpZw'

nice_token = re.compile(r"^\w+[\w':;.,?!]*$", flags=re.UNICODE)

# This is the listener, resposible for receiving data
class StdOutListener(tweepy.StreamListener):
    def on_status(self, status):
        print(ascii(status.text))
        tokenizza(status.text)
'''        
    def on_data(self, data):
        # Twitter returns data in JSON format - we need to decode it first
        decoded = json.loads(data)

        # Also, we convert UTF-8 to ASCII ignoring all bad characters sent by users
        print( '@%s: %s' % (decoded['user']['screen_name'], decoded['text'].encode('ascii', 'ignore')))
        print('')
        return True

    def on_error(self, status):
        print(status)
'''

def test(token):
	return nice_token.match(token) is not None and token != u'rt'

def purge(token):
	x = None
	while token[-1] in "';:,.?!":
		x = token[-1]
		token = token[:-1]
		if x == ';':
			x = ':'
	return token, x

def stringa(tupla):
	x = ' '.join(tupla)
	if len(x) >= 2 and x[-2] == ' ' and x[-1] in '?!.:':
		return x[0:-2] + x[-1]
	return x

def tokenizza(testo):
	token_list = testo.lower().split()
	multigram = []
	last_insert = -1
	for i, token in enumerate(token_list):
		if last_insert == i - 2:
			multigram.append('-')
		if test(token):
			last_insert = i
			if i == 0 or (multigram and multigram[-1] == '^'):
				multigram.append('$')

			tok, last = purge(token)
			multigram.append(tok)
			if last:
				multigram.append(last)
				if last in "?!.":
					multigram.append('^')
			elif i == len(token_list) -1 and multigram[-1] != '^':
				multigram.append('^')

	print(';;;;;;;;;;;;;')
	print(multigram)
	print(';;;;;;;;;;;;;')

	cache = []
	result = []
	multigram.append('-')
	for unigram in multigram:
		if unigram != '-':
			cache.append(unigram)
		else:
			while len(cache) > 4:
				prev = (cache.pop(0), cache.pop(0))
				middle = cache[:-2]
				next = list(cache[-2:])
				while middle:
					result.append((prev[0], prev[1], stringa(middle), next[0], next[1], len(middle)))
					next[1] = next[0]
					next[0] = middle.pop()
			if len(cache) == 4:
				result.append((cache[0], cache[1], '', cache[2], cache[3], 0))
			cache = []
	sql_cur.executemany('INSERT INTO multigrammi VALUES (?, ?, ?, ?, ?, ?)', result)


if __name__ == '__main__':
    l = StdOutListener()
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    print("Showing all new tweets for #programming:")

    # There are different kinds of streams: public stream, user stream, multi-user streams
    # In this example follow #programming tag
    # For more details refer to https://dev.twitter.com/docs/streaming-apis
    stream = tweepy.Stream(auth, l)
    #stream.filter(stream.filter(track=['#mlb']))
    stream.sample()
