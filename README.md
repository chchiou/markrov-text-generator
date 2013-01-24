A Random Text Generator based on Markrov Chains
===============================================

What's a Markrov Chain?
-----------------------

Yep, the `r` is there on purpuose.

If you already know what a Markov Chain is and 
how you can use it to generate random text, 
then skip the next paragraph.

### Markov Chains ###
A Markov Chain is a way of representing certain 
stochastic processes as probabilistic automatons.

You can use Markov Chains to generate random text 
which looks like it's been translated on babelfish 
back and forth multiple times.

Read more about Markov Chains:
http://en.wikipedia.org/wiki/Markov_chain

## Markrov Chains ##

*First of all, yes, the name is made up.*

A Markrov Chains is a Markov Chain that has an 
extra twist: it can jump trough iperspace and
generate better text than normal Markov Chains would.
How? By cheating of course!

The idea is simple:

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

And when you compose the text just remember to add 
the extra words.

## Enough with the theoretical formalisms, show me the code! ##

This is a more complex implementation: it's a second order 
Markrov Chain (it jumps from couple to couple of words) 
that trains on tweets taken from the Twitter Streaming API.

It also parses the tweet to leverage on its syntax 
(punctuation mainly) in order not to mess too much the meaning up.

There are some more secret tricks to get better (= funnier) text. 
If you want to know more read `markrov-text-generator.pdf`, it's in the repo
(of course you need to understand Italian, but that's just a detail!).

## Implementation details and requirements ##
2 python scripts: one feeds the database from twitter, one generates text.

**Requirements:** 
- Python 2.7
- tweepy (and API keys)
- sqlite3

## Instructions ##

1. Get the API keys from Twitter and put them in `token-stream.py` *(you can find lots of guides on how to do that)*
2. Launch token-stream.py and let it gather tweets for some time (careful, your database is gonna get fat fast)
3. Open a python shell and `import markov.py`. Generate delirious sentences by calling `generate('$')` you can also use different starting points, just type the word you'd like the sentence to start with (`$` means to start from any sentence).
4. ???
5. PROFIT?
