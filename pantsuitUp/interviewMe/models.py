# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.conf import settings

import pyttsx
import speech_recognition as sr
import string
import nltk
import indicoio
import time
import re
import random
import json
import os


class Tagger(models.Model):
	""" Parse input text file of questions and create 
		json of Question Dictionaries (question_text, labels)."""

	def split_question(self, question):
		labels_difficulty = ["easy", "medium", "hard"]
		labels_length = ["short", "medium", "long"]
		labels_category = ["Interpersonal Skills", "Leadership", "Failure_Frustration", "Time Management_Prioritization"]
		""" Split and return labels for each question. """
		question_and_labels = re.split('(?<=[.!?]) +',question)
		tags = re.sub('[(){}<>]', '', question_and_labels[1])
		tags = tags.split(", ")
		tags = [tag for tag in tags if tag is not None] 
		if len(tags) == 3:
			tags[0] = labels_difficulty.index(tags[0])
			tags[1] = labels_length.index(tags[1])
			tags[2] = labels_category.index(tags[2])
			return (question_and_labels[0], tags)

	def json_build(self, questions_l):
		""" Save each question and labels in dictionary, 
			and save collection of dictionaries in list. """
		questions_final = {}
		questions_dict = {}
		for i, question in enumerate(questions_l):
			questions_tags_dict = {}
			self.split_question(question)
			if self.split_question(question):
		 		(question_text, tags) = self.split_question(question)
		 		questions_tags_dict["text"] = question_text
		 		questions_tags_dict["labels"] = tags

		 		questions_dict["Question %d" % (i+1)] = questions_tags_dict
		questions_final["questions"] = questions_dict
		questions_json = json.dumps(questions_final)
		return questions_json

	def tagger(self):
		""" Read from question file, parse text, and save list of	individual questions. """
		q = []
		with open(os.path.join(settings.PROJECT_ROOT, 'questions.txt'), 'r') as questions_all:
			for question in questions_all:
				que = question.strip()
				if que:
					question = re.sub('[/]', '', question)
					q.append(question.strip())
			q = [x for x in q if x is not None]
			return self.json_build(q)

class Randomizer(models.Model):
	""" Randomize combination of difficulty, length, and category
		and select 3 questions to ask in interview. """

	def genRand(self,a,b):
		""" Generate random int i from range a <= i <= b. """
		return random.sample(xrange(a,b), 1)[0]

	def randomize(self):
		""" Generate random combination of difficulty, length, and category. """
		difficulty = self.genRand(0,2)
		length = self.genRand(0,2)
		category = self.genRand(0,3)
		return [difficulty, length, category]

	def get_q(self, questions_d, comb):
		""" Fetch question text given random combination. """
		for que in questions_d["questions"]:
			if comb == questions_d["questions"][que]["labels"]:
				return questions_d["questions"][que]["text"]			

	def main(self):
		""" Check to see if combination doesn't match label in question dict or
			if combination has been used before. 
			If so, try another random combination.
			If not, save question text to list.
			Output list of three questions. """
		three_q = []
		labels = ["first", "second", "third"]
		t = Tagger().tagger()
		q_dict = json.loads(t)

		while (len(three_q) < 4):
			comb = self.randomize()
			if self.get_q(q_dict, comb):
				if self.get_q(q_dict, comb) not in three_q:
					three_q.append(self.get_q(q_dict, comb))
				else:
					self.get_q(q_dict, self.randomize())
			else:
				self.get_q(q_dict, self.randomize())
		return three_q

class Interview(models.Model):
	intro = models.CharField(max_length = 100000, default = "Hello and welcome. Let's get started. ")
	conclusion = models.CharField(max_length = 100000, default = "Goodbye")
	question_1 = models.CharField(max_length = 100000, default = "What's your greatest weakness?")
	question_2 = models.CharField(max_length = 100000, default = "Describe a team you showed leadership.")
	question_3 = models.CharField(max_length = 100000, default = "What's your work-style?")

	def generate_interview(self):
		self.pick_seqs()
		self.pick_questions()

	def say_something(self, text):
		engine = pyttsx.init()
		engine.setProperty("",120)
		for voice in voices: #3
		   engine.setProperty('voice', voice.id)
		   engine.say('The quick brown fox jumped over the lazy dog.')
		engine.runAndWait()

		engine.say(text)
		engine.runAndWait()

	def say_intro(self):
		self.say_something(self.intro)

	def say_conclusion(self):
		self.say_something(self.conclusion)

	def ask_question(self, question):
		self.say_something(question)

	def pick_questions(self):
		r = Randomizer()
		question_list = r.main()
		self.question_1 = question_list[0]
		self.question_2 = question_list[1]
		self.question_3 = question_list[2]

	def pick_seqs(self):
		seq_1 = ("Thank you for coming today. I'm Siera, and I'll be your interviewer. I've been with Amazon for the past 5 years, and I'm currently a project manager. Today is about getting to know you a little bit better. I'll ask you a few questions to learn more about you and what you've been working on. At the end there will be time for questions and feedback. Does that sound ok?", "Well, that brings us to the end of the interview. Thank you so much for the information you provided! I'll be bringing my notes to my supervisor and emphasize all of the amazing projects you shared with me today. You should be hearing back from us in the next few days - I look forward to seeing you soon!")
		seq_2 = ("Ok, let's get started. I'm going to ask you a few questions to see how you'll fit with the team.", " Ok, thanks for your time. We'll let all applicants know by the end of next month. Have a good day.")
		seq_3 = ("Thanks for coming. I'm Siera, and I'll be your interviewer. I majored in computer science and have worked at a few different companies since then. I've been with Amazon for the past few years and I love it. I work on a team of product developers. My team has about 10 members, and we work on getting products ready for market. It's really interesting because I get to work with all branches of the company and see a product from start to finish. This is the team youll be interviewing for - we normally like students to have a large amount of project work and leadership.", "Wow, that was great. I loved speaking with you today. Thank you so much for your interest in the company. I'll pass your resume around to my supervisors. Please apply online, and have a great day!")
		seq_4 = ("Hello. Do you have a copy of your resume? It says here you are interested in our company - can you tell me why?", "Ok, that brings us to the end of the interview. Please make sure you have completed the online application. We'll be in touch soon.")
		seq_5 = ("Hello, the interview today will be in the STAR format. STAR stands for Situation, Task, Action, and Results. In all answers, please follow this format, focusing specifically on what you contributed.", "Ok, thanks for your time. I'll give you my business card. Please reach out if you have any more questions. It was great speaking with you today.")
		seq_list = [seq_1, seq_2, seq_3, seq_4, seq_5]
		seq_ind = random.randint(0,4)
		seq_pair = seq_list[seq_ind]
		self.intro = seq_pair[0]
		self.conclusion = seq_pair[1]


@python_2_unicode_compatible
class SpeechRec(models.Model):
	output_text = models.CharField(max_length = 100000, default = "")

	def __str__(self):
		return self.output_text

	def get_microphone_output(self):
		'''
		Runs a speech recognition library and returns a string of user's phrase after an user stops talking
		'''
		r = sr.Recognizer()
		sr.dynamic_energy_threshold = False
		sr.energy_threshold = 500
		tries = 3
		answer = ""

		with sr.Microphone() as source:
		    while True:
		        r.adjust_for_ambient_noise(source)
		        audio = r.listen(source)
		        try:
		            snippet = r.recognize_google(audio)
		            answer += " " + snippet
		            print answer
		            if "answer" in snippet:
		                return answer
		        except sr.UnknownValueError:
		            if tries == 0:
		                return "Google doesn't understand audio"
		            tries -= 1
		        except sr.RequestError as e:
		            return e


@python_2_unicode_compatible
class Feedback(models.Model):
	input_text = models.CharField(max_length = 100000, default = "")
	feedback_text = models.CharField(max_length = 10000, default = "feedback")
	raw_sentiment = models.DecimalField(max_digits = 3, decimal_places = 2, default = .5)
	raw_personality = models.DecimalField(max_digits = 3, decimal_places = 2, default = .5)
	raw_ownership = models.DecimalField(max_digits = 3, decimal_places = 2, default = .5)
	raw_passivity = models.DecimalField(max_digits = 3, decimal_places = 2, default = .5)
	
	def __str__(self):
		return self.input_text

	def process_text(self):
		text = self.input_text
		if len(text) == 0:
			return

		indicoio.config.api_key = '7b7ddd4e3120df54b1a4018d77e01f9c'

		word_dict, total_words = self.word_freq(text)
		self.raw_sentiment = self.sentiment_measure(text)
		self.raw_personality = self.personality_measure(text)
		self.raw_ownership = self.ownership_measure(word_dict)
		self.raw_passivity = self.passive_measure(text)
		raw_overused_words = self.overused_words(word_dict, total_words)

		personality = self.convert_personality(self.raw_sentiment, self.raw_personality)
		ownership = self.convert_ownnership(self.raw_ownership)
		passivity = self.convert_passivity(self.raw_passivity)
		overused_words = self.convert_overused_words(raw_overused_words)

		self.feedback_text = self.give_feedback(ownership, passivity, personality, overused_words)

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

	def give_feedback(self, ownership, passivity, personality, overused_words):
		start = "Let's talk about how that went. I scored your interview based on a few metrics, including how often you used the passive voice, how often you used certain words, various personality traits your answers showed, and finally how much ownership you took of your work. These areas are often where women are weaker than their male counterparts."
		ownership_text = " Let's start with your use of I vs We pronouns. In interviews, you want to make it clear that you are the one at the center of your experiences - interviewers do not care about your teammate's accomplishments. " + ownership
		passivity_text = " Now, let's discuss your use of the passive voice. Using the passive voice instead of the active voice can make it seem as if you are not confident about what you are saying. " + passivity
		personality_text = " It's also important to understand how your answers shape the way people see you. In this interview, you came across as " + personality[0] + personality[1]
		overuse_text = " Finally, repeating words can emphasize points, but also become distracting. " + overused_words
		end = " Thank you for practicing with me today. If you wish to practice again, click the back button. Otherwise, good luck!"
		text = start + ownership_text + passivity_text + personality_text + overuse_text + end
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
		text_wo_punc = text.translate(string.punctuation)

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
