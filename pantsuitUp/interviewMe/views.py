# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from .models import Feedback

# Create your views here.

def home(request):
	return render(request, 'interviewMe/index.html', {})

def about(request):
	return render(request, 'interviewMe/about.html', {})

def interview(request):
	return render(request, 'interviewMe/feedback.html', {})

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
	return HttpResponse(feedback.feedback_text)