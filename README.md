A Random Text Generator based on Markrov Chains
===============================================

What's a Markrov Chain?
-----------------------

Yep, the `r` is there on purpose.

If you already know what a Markov Chain is and 
how you can use it to generate random text, 
then skip the next paragraph.

### Markov Chains ###
A Markov Chain is a way of representing certain 
stochastic processes as probabilistic automatons.

You can use Markov Chains to generate random text 
which looks like it's been either translated back and 
forth trough babelfish (first order), 
or it is the result of rearranging the lines of a book (higher orders).

Read more about Markov Chains:
http://en.wikipedia.org/wiki/Markov_chain

## Markrov Chains ##

*First of all, yes, the name is made up, it's a mix between Markov and my surname.*

A Markrov Chains is a Markov Chain that has an 
extra twist: it can jump trough hyperspace and
generate better text than normal Markov Chains would.
How? By cheating of course!

The idea is simple.

Given the following training sentece (by Linus):

`MAURO SHUT THE FUCK UP`

A first order Markov Chain memorizes the following 
possible transitions:

	MAURO 	==> 	SHUT
	SHUT 	==> 	THE
	THE 	==> 	FUCK
	FUCK 	==> 	UP

A Markrov Chain also learns the following transitions:

	MAURO 	=(SHUT THE FUCK)=>	UP
	MAURO	=(SHUT THE)=>		FUCK
	MAURO	=(SHUT)=>			THE
	SHUT	=(THE FUCK)=> 		UP
	SHUT	=(THE)=>			FUCK
	THE 	=(FUCK)=>			UP

Please notice the hyperspace jump. Also, when you compose 
the text don't forget to add the extra words.

## Enough with the theoretical formalisms, show me the code! ##

This is a more complex implementation: it's a second order 
Markrov Chain (it jumps from couple to couple of words) 
that trains on tweets taken from the Twitter Streaming API.

It also parses the tweet to leverage on its syntax 
(punctuation mainly) in order not to mess up the meaning too much.

There are some more secret tricks to get better (= funnier) text. 
If you want to know more read `markrov-text-generator.pdf`, it's in the repo.


*Of course you need to understand Italian, but that's a minor detail! 
Just wear your best moustache and gesticulate while reading it out loud, you will easily understand it, trust me!*

## Implementation details and requirements ##
2 python scripts: one feeds the database from twitter, the other generates text.
1 empty SQLite3 database.

**Requirements:** 
- Python 2.7
- tweepy (and Twitter API keys)
- sqlite3


### A WORD OF CAUTION: ###
This might not be the worst implementation you're gonna find 
on github and it does scale up to few GBs of data 
(I personally got the DB up to ~5GB) but there's a lot of dumb crap in here.
It was a project worth 2 points/credits/dunno-how-people-call-them, 
which is very little if you don't know and means that I couldn't spend too much time building it (I didn't even build it alone).
Also, Markrov Chains might aswell be a real thing, with a proper name
and proper theory. I don't know. If that's not the case remember 
to commend me for the next Turing Award!


## Instructions ##

1. Get the API keys from Twitter and put them in `token-stream.py` *(you can find lots of guides on how to do that)*
2. Launch `token-stream.py` and let it gather tweets for some time (careful, your database is gonna get fat fast)
3. Open a python shell and `import markov.py`. Generate delirious sentences by calling `generate('$')` you can also use different starting points, just type the word you'd like the sentence to start with (`$` means to start from any sentence).
4. ???
5. PROFIT?
6. *Please let me know if you find any extraordinarly funny sentence! (PROFIT!)*

A quote from a text generated trough this script, to give you a more complete understanding of the cosmos:
	
	I'm not fucking rocket science!


