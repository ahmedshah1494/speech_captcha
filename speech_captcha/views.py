# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
import time
from django.core.files.storage import FileSystemStorage
from features import extractFeatures
import gmm
from captcha import settings
from django.http import HttpResponse
import json
import speech_recognition as sr
from captcha import settings
from speech_captcha.models import *
import random
import editdistance
from django.middleware.csrf import get_token
# Create your views here.
def enroll_corpus(request):
	if request.method == 'GET':
		return render(request, 'enroll_corpus.html', {})
	f = request.FILES['transcript']
	print file
	context = {}
	try:
		new_corpus = Corpus(name=request.POST['corpus_name'],
							language=request.POST['language'])
		new_corpus.save()
		line = f.readline()
		while line:
			length = line.find('(') if line.find('(') > 0 else None
			transcript = line[: length]
			new_sent = Sentence(transcript=transcript,
								corpus=new_corpus)
			new_sent.save()
			line = f.readline()
		context['response'] = 'Corpus successfully enrolled!'
	except e:
		print e
		context['error'] = 'Corpus enrollment failed!' 
	return render(request, 'enroll_corpus.html', context)


def home(request):
	sentences = Sentence.objects.all()
	sentence = sentences[random.randint(0, len(sentences))].transcript.lower()
	return render(request, "basic_index.html", {'sentence': sentence})

def getSentence(request):
	sentences = Sentence.objects.all()
	sentence = sentences[random.randint(0, len(sentences))].transcript.lower()
	resp = """
	<h3>{0}</h3>
    <form enctype="multipart/form-data" method="post" action='/captcha/upload_audio'>
        <input name='transcript' type='hidden' value='{0}' ></input>
        <input name='speech' type="file" accept="audio/*;capture=microphone"></input>
        <input type="submit" name="submit"></input>
        <input type="hidden" name="csrfmiddlewaretoken" value="{1}">
    </form>
	""".format(sentence, str(get_token(request)))
	return HttpResponse(resp, content_type='text/html')

def LER(filename, transcript):
	r = settings.RECOGNIZER
	with sr.AudioFile(filename) as source:
		audio = r.record(source)
	text = r.recognize_sphinx(audio)
	ler = editdistance.eval(text, transcript)
	ler = float(ler) / len(transcript)
	return ler, transcript
def process_audio(request):
	file = request.FILES['speech']
	fs = FileSystemStorage()
	filename = "temp_%d.wav" % time.time()
	filename = fs.save(filename, file)
	feats = extractFeatures("%s/%s" % (fs.location, filename), scmc=True)
	f_label = gmm.test(feats, 256, settings.GMM_ROOT)
	# r = settings.RECOGNIZER
	# with sr.AudioFile("%s/%s" % (fs.location, filename)) as source:
	# 	audio = r.record(source)
	# transcript,score = r.recognize_sphinx(audio)
	ler, transcript = LER("%s/%s" % (fs.location, filename), 
							request.POST['transcript'])
	r_label = ler < settings.RECOGNITION_THRESH
	context = {"label": "passed" if r_label and f_label else "failed",
				"transcript": transcript,
				"score":ler}
	resp = json.dumps(context)
	# return render(resp, content_type='application/json')
	return render(request, "basic_index.html", context)
    
