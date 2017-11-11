"""
Whack 2017 Alexa
Hour 1
Text Analysis for Length, 
Speed, and Sentiment.
"""

import indicoio
import time
import re
import spacy
indicoio.config.api_key = '7b7ddd4e3120df54b1a4018d77e01f9c'

test_paragraph = open('pride.txt','r').read()

# Sentiment
def sentiment_analysis(string):
	return indicoio.sentiment(string)
print sentiment_analysis(test_paragraph)


# Length
# helper functions
def time_to_s(minute):
	return minute * 60

def time_to_m(second):
	return second / 60
# main
def length_analysis(string):
	start_time = time.time()
	f = open('pride.txt', 'r')
	end_time = time.time()

	return end_time - start_time

print time_to_m(length_analysis(test_paragraph))


# Speed
def speed_analysis(string):
	passage_word = []
	parsed_string = re.sub(r'[^\w\s]','',string)	
	passage_word = parsed_string.split(" ")
	return length_analysis(string) / float(len(passage_word))
	
print speed_analysis(test_paragraph)


# Passive Voice
def passive_analysis(string):
	passive_voice = {'passive': 0}
	passive_verb = ['is','are','am','was','were','had','has','have']
	passage_sent = re.split('(?<=[.!?]) +',string)
	for sent in passage_sent:
		passage_word_sent = sent.split(" ")
		for i, word in enumerate(passage_word_sent):
			if word in passive_verb:
				if (passage_word_sent[i+1][-3:] == 'ing') or (passage_word_sent[i+1][-2:] == 'en') or (passage_word_sent[i+1][-2:] == 'ed'):
					passive_voice['passive'] += 1

	return passive_voice['passive'] / float(len(passage_sent))
print passive_analysis(test_paragraph)
