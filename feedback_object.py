"""
Feedback object -- might make sense for calculations to go here too
"""

import string
import nltk
import indicoio
import time
import re

class Feedback(object):

	def __init__(self, text):
		indicoio.config.api_key = '7b7ddd4e3120df54b1a4018d77e01f9c'

		word_dict, total_words = self.word_freq(text)
		raw_sentiment = self.sentiment_measure(text)
		raw_personality = self.personality_measure(text)
		raw_ownership = self.ownership_measure(word_dict)
		raw_passivity = self.passive_measure(text)
		raw_overused_words = self.overused_words(word_dict, total_words)

		self.personality = self.convert_personality(raw_sentiment, raw_personality)
		self.ownership = self.convert_ownnership(raw_ownership)
		self.passivity = self.convert_passivity(raw_passivity)
		self.overused_words = self.convert_overused_words(raw_overused_words)

	def convert_personality(self, sentiment, personality):
		"""
		Returns tuple of a string of personality traits and a string of the combined advice corresponding to those traits
		"""
		personality_string = ""
		advice_string = ""

		# polarity
		if sentiment < .5:
			personality_string += "negative, "
			advice_string += "You should keep your answers hopeful and focus on the positive outcomes of experiences. "
		else:
			personality_string += "positive, "
			advice_string += "People probably feel that you would bring a positive presence to the company. "
		
		# openness 
		if personality["openness"] < .5:
			personality_string += "close-minded, "
			advice_string += "You should be more flexible and open to other ideas. You'll come across as more humble and seem easier to work with."
		else:
			personality_string += "open-minded, "
			advice_string += "You come across as someone who is flexible and open to new ideas. "
		
		# agreeable
		if personality["agreeableness"] < .5:
			personality_string += "disagreeable, "
			advice_string += "You should use more enthusiastic language and emphasize examples of cooperation. "
		else:
			personality_string += "agreeable, "
			advice_string += "Coworkers likely find you easy to work with. "

		# conscientious
		if personality["conscientiousness"] < .5:
			personality_string += "and not conscientious. "
			advice_string += "You should more examples of taking other peoples feelings into account or adapting your approach to suit them better to show that you are thoughtful."
		else:
			personality_string += "and conscientious. "
			advice_string += "You seem thoughtful and come across as a nice teammate."

		return personality_string, advice_string

	def convert_ownnership(self, ownership):
		if ownership < .3:
			return "You said we very often, which discounts your role in projects and teams. Try using first person pronouns more to claim ownership of what you have done"
		if ownership < .7:
			return "You almost always took ownership. You emphasized your role, but still attributed your accomplishments to others occasionally."
		return "You always took ownership! It was clear what your contributions were and the impact you had"

	def convert_passivity(self, passivity):
		if passivity < .3:
			return "You rarely used the passive voice. It made it seem like you were confident about what you were saying."
		return "You often used the passive voice. Attempting to use the active voice will make you sound more confident."	

	def convert_overused_words(self, overused_words):
		if len(overused_words) != 0:
			word_string = "The words you said most in the interview include "
			for n in range(len(overused_words) - 1):
				word_string += overused_words[n] + ", "
			word_string += "and " + overused_words[-1] + ". Try to say these words less often to show a varied vocabularly. "
			return word_string
		else:
			return "You did not have any overused words in your answers. Good job!"

	def give_feedback(self):
		start = "Let's talk about how that went. I scored your interview based on a few metrics, including how often you used the passive voice, how often you used certain words, various personality traits your answers showed, and finally how much ownership you took of your work. These areas are often where women are weaker than their male counterparts."
		ownership = " Let's start with your use of I vs We pronouns. In interviews, you want to make it clear that you are the one at the center of your experiences - interviewers do not care about your teammate's accomplishments. " + self.ownership
		passivity = " Now, let's discuss your use of the passive voice. Using the passive voice instead of the active voice can make it seem as if you are not confident about what you are saying. " + self.passivity
		personality = " It's also important to understand how your answers shape the way people see you. In this interview, you came across as " + self.personality[0] + self.personality[1]
		overuse = " Finally, repeating words can emphasize points, but also become distracting. " + self.overused_words
		end = " If you would like to see your detailed results, please visit the website PANTSUITUP.ORG. Thank you for practicing with me today. If you wish to practice again, say XXXX. Otherwise, good luck!"
		text = start + ownership + passivity + personality + overuse + end
		return text


	"""**************** CALCULATION FUNCTIONS BELOW ****************"""

	def sentiment_measure(self, text):
		"""
		Uses Indico Sentiment Analysis API to find postivity-negativity value of text
		"""
		return indicoio.sentiment(text)

	def personality_measure(self, text):
		return indicoio.personality(text)


	def word_freq(self, text):
		"""
		Creates and returns a dictionary of words mapped to their frequencies as well as the total number of words
		"""
		word_dict = dict()
		text_wo_punc = text.translate(None, string.punctuation)

		# download nltk packages first time running program
		try:
			word_list = nltk.pos_tag(nltk.word_tokenize(text_wo_punc))
		except:
			nltk.download('punkt')
			nltk.download('averaged_perceptron_tagger')
			word_list = nltk.pos_tag(nltk.word_tokenize(text_wo_punc))

		for word, pos in word_list:
			if word in word_dict:
				word_dict[word] += 1
			elif pos != 'CC' and pos != 'IN' and pos != 'TO' and pos != 'DT': # exclude prepositions, conjunctions, etc
				word_dict[word] = 1

		return word_dict, len(word_list)

	def ownership_measure(self, word_dict):
		""" 
		Calculates and returns measure of ownership as judged by frequency of first_person vs second_person pronouns used
		"""
		first_person = 0
		second_person = 0

		if "I" in word_dict:
			first_person += word_dict["I"]
		if "me" in word_dict:
			first_person += word_dict["me"]
		if "my" in word_dict:
			first_person += word_dict["my"]
		if "we" in word_dict:
			second_person += word_dict["we"]
		if "us" in word_dict:
			second_person += word_dict["us"]
		if "our" in word_dict:
			second_person += word_dict["our"]

		return (float(first_person) / (second_person + first_person))

	def passive_measure(self, text):
		"""
		Measures proportion of passive sentences to all sentences
		"""
		passive_voice = {'passive': 0}
		passive_verb = ['is','are','am','was','were','had','has','have']
		passage_sent = re.split('(?<=[.!?]) +',text)
		for sent in passage_sent:
			passage_word_sent = sent.split(" ")
			for i, word in enumerate(passage_word_sent):
				if word in passive_verb:
					if (passage_word_sent[i+1][-3:] == 'ing') or (passage_word_sent[i+1][-2:] == 'en') or (passage_word_sent[i+1][-2:] == 'ed'):
						passive_voice['passive'] += 1

		return passive_voice['passive'] / float(len(passage_sent))

	def overused_words(self, word_dict, total_words):
		""" 
		Finds words that makes up more than 1% of a person's answers and returns them as a list of overused words
		"""
		overused_words_list = []
		
		if total_words > 500:
			threshold = .01
		else:
			threshold = .05
		
		for word, count in word_dict.iteritems():
			if (count / float(total_words)) > threshold: 
				overused_words_list.append(word)

		return overused_words_list

sample_1 = "At my current position, I am part of the team that coordinates the company lunch-and-learn sessions. Each week, we meet to brainstorm who would be exciting guest speakers. We all work together to ensure a diverse mix of speakers, aiming to appeal to a wide swath of people in the company. Because everyone on the team comes from different areas within the company, we have all learned so much about big ideas, from marketing to tech."

feedback = Feedback(sample_1)
print feedback.give_feedback()