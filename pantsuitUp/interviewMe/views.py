# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from .models import SpeechRec, Feedback, Interview


def do_interview(request):
	interview = Interview()
	interview.generate_interview()
	sr = SpeechRec()
	combined_answers = ""
	
	interview.say_intro()
	interview.ask_question(interview.question_1)
	combined_answers += sr.get_microphone_output() + ". "
	interview.ask_question(interview.question_2)
	combined_answers += sr.get_microphone_output() + ". "
	interview.ask_question(interview.question_3)
	combined_answers += sr.get_microphone_output()

	return feedback(request, combined_answers)


def submit_info(request):
	if request.method == 'POST':
		form = request.POST
	else:
		form = request.GET
	return interview(request, form)



# this view + template exists solely for start-up on heroku (to add interviewMe/ prefix)
def start(request):
	return render(request, 'interviewMe/start.html', {})

def home(request):
	return render(request, 'interviewMe/index.html', {})

def about(request):
	return render(request, 'interviewMe/about.html', {})

def interview(request, name = "Rachel"):
	interview = Interview()
	speech_rec_obj = SpeechRec()
	context = {"interview": interview,
			   "speech_rec_obj": speech_rec_obj,
			   "name": name
			   }
	return render(request, 'interviewMe/interview.html', context)

def features(request):
	return render(request, 'interviewMe/features.html', {})

def demo(request):
	return render(request, 'interviewMe/demo.html', {})

def login(request):
	return render(request, 'interviewMe/login.html', {})

def feedback(request, input_text = "I love dogs"):
	feedback = Feedback()
	feedback.input_text = input_text
	feedback.process_text()
	context = {"passivity_score": int(feedback.raw_passivity * 100),
			   "positivity_score": int(feedback.raw_sentiment * 100),
			   "agreeableness_score": int(feedback.raw_personality["agreeableness"] * 100),
			   "openness_score": int(feedback.raw_personality["openness"] * 100),
			   "conscienciousness_score": int(feedback.raw_personality["conscientiousness"] * 100),
			   "ownership_score": int(feedback.raw_ownership * 100),
			   "feedback_text": feedback.feedback_text
				}
	return render(request, 'interviewMe/feedback.html', context)
