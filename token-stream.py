# -*- coding: utf_8 -*-

import tweepy, re

import sqlite3
sql_conn = sqlite3.connect('tweets.db', isolation_level=None )
sql_cur = sql_conn.cursor()

## API KEY SETTINGS
auth1 = tweepy.auth.OAuthHandler('YOUR KEY','YOUR KEY')
auth1.set_access_token('YOUR KEY','YOUR KEY')
############

api = tweepy.API(auth1)


nice_token = re.compile(r"^\w+[\w':;.,?!]*$", flags=re.UNICODE)

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

	print ';;;;;;;;;;;;;'
	print multigram
	print ';;;;;;;;;;;;;'

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


class StreamListener(tweepy.StreamListener):
	def on_status(self, status):
		print status.text
		print r"\\\\\\ "
		tokenizza(status.text)
		print r'////// '

def main():
	l = StreamListener()
	streamer = tweepy.Stream(auth=auth1, listener=l, timeout=3000000000 )
	streamer.sample()


if __name__ == '__main__':
	try:
		main()
	except (KeyboardInterrupt, SystemExit):
		sql_cur.close()
		sql_conn.close()
		print '\nOK, bye'
