import string
import nltk

sample_1 = "At my current position, I am part of the team that coordinates the company lunch-and-learn sessions. Each week, we meet to brainstorm who would be exciting guest speakers. We all work together to ensure a diverse mix of speakers, aiming to appeal to a wide swath of people in the company. Because everyone on the team comes from different areas within the company, we have all learned so much about big ideas, from marketing to tech."

sample_2 = "At my current position, I am part of like the team that coordinates like the company lunch-and-learn sessions. Each week, we meet to try to brainstorm who would be exciting guest speakers. We all like work together to try to ensure a diverse mix of speakers, aiming to appeal to try to like a wide swath of people in the company. Because everyone on the team comes from like different areas within the company, we have all like learned so much about big ideas, from marketing to like tech"


def word_freq(text):
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

def overused_words(word_dict, total_words):
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

def ownership_measure(word_dict):
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
	

if __name__ == "__main__":
	word_dict, total_words = word_freq(sample_2)
	# print overused_words(word_dict, total_words)
	# print ownership_measure(word_dict)



