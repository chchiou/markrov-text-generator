# -*- coding: utf_8 -*-

import sqlite3, random, re

spl_conn = sqlite3.connect('tweets.db')
spl_cur = spl_conn.cursor()

def generate(word):

	init = nnext = next = word
	tweet_stack = []
	mode = 2
	nexts = ricerca_new(mode, next)
	pprev, prev, middle, next, nnext, ms = nexts
	text = [pprev, prev, middle, next, nnext]
	tweet_stack.insert(0, text)
	cs =  0
	while next != '^' and nnext != '^':
		nexts = ricerca_new(mode, next, nnext)
		try:
			pprev, prev, middle, next, nnext, ms = nexts
			text = [middle, next, nnext]
			tweet_stack.insert(0, text)
		except:
			cs += 1
			try:
				tweet_stack.pop()
				middle, next, nnext = tweet_stack[0]
			except:
				cs = 0
				nnext = next = init
				nexts = ricerca_new(mode, next)
				pprev, prev, middle, next, nnext, ms = nexts
				text = [pprev, prev, middle, next, nnext]
				tweet_stack.insert(0, text)

	tweet = ''
	for part in reversed(tweet_stack):
		tweet += ' '.join(part)
		tweet += ' '
	tweet = tweet.replace("^", "")
	tweet = tweet.replace(" $", "")
	tweet = tweet.replace(" ,", ",")
	tweet = tweet.replace(" .", ".")
	tweet = tweet.replace(" ?", "?")
	tweet = tweet.replace(" !", "!")
	tweet = tweet.replace(" :", ":")
	tweet = tweet.replace("  ", " ")
	tweet_cap = re.split('([.!?] *)', tweet)
	after_up = ""
	for each in tweet_cap:
		for i, c in enumerate(each):
			if c.islower():
				break
	
		after_up += each[:i] + each[i:].capitalize()

	tweet = "".join([part for part in after_up])

	print tweet

	# spl_cur.close()
	# spl_conn.close()

def ricerca_new(mode, pprev, prev=None):
	try:
		if prev:
			spl_cur.execute("select middle_size from multigrammi where (pprev = ? and prev = ?)", (pprev, prev))
		else:
			spl_cur.execute("select middle_size from multigrammi where (pprev = ?)", (pprev,))
		fetch = spl_cur.fetchall()
		size = [x for (x, ) in fetch]

		if size == [] or size == [0]:
			return None
		size.sort()
		beta = len(size)
		mode = 1.0/35*beta
		 
		if beta >= mode:
			triang = size[int(random.triangular(0, beta, mode))]
		else:
			triang = beta
		
		if prev:
			spl_cur.execute("select * from multigrammi where (pprev = ? and prev = ? and middle_size = ?)", (pprev, prev, triang))
		else:
			spl_cur.execute("select * from multigrammi where (pprev = ? and middle_size = ?)", (pprev, triang))
	except Exception as e:
		print e
		print '!!! ', next
	multi = random.choice(spl_cur.fetchall())
	return multi
