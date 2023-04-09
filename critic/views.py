from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.http import HttpResponseForbidden
from account.models import Profile, Role
from django.contrib import messages
from movies.models import Movie, Review
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords
import re
from joblib import load
from sys import path
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent

# Create your views here.
def index(request):
    if(request.session.has_key('account_id')):
        if(request.session['account_role'] == 2):
            content = {}
            content['title'] = 'Welcome ' + request.session['account_name']
            content['my_reviews'] = Review.objects.filter(critic = int(request.session['account_id']))
            return render(request, 'critic/index.html', content)
        else:
            return HttpResponseForbidden()
    else:
        return HttpResponseRedirect(reverse('account-login'))

def movies(request):
    if(request.session.has_key('account_id')):
        if(request.session['account_role'] == 2):
            content = {}
            content['title'] = 'Movies'
            content['movies'] = Movie.objects.all().order_by('name')
            return render(request, 'critic/movies.html', content)
        else:
            return HttpResponseForbidden()
    else:
        return HttpResponseRedirect(reverse('account-login'))

#Removal of HTML Contents
def remove_html(text):
    soup = BeautifulSoup(text, "html.parser")
    return soup.get_text()

#Removal of Punctuation Marks
def remove_punctuations(text):
    return re.sub('\[[^]]*\]', '', text)

# Removal of Special Characters
def remove_characters(text):
    return re.sub("[^a-zA-Z]", " ", text)

#Removal of stopwords
def remove_stopwords_and_lemmatization(text):
    final_text = []
    text = text.lower()
    text = nltk.word_tokenize(text)

    for word in text:
        if word not in set(stopwords.words('english')):
            lemma = nltk.WordNetLemmatizer()
            word = lemma.lemmatize(word)
            final_text.append(word)
    return " ".join(final_text)


#Total function
def cleaning(text):
    text = remove_html(text)
    text = remove_punctuations(text)
    text = remove_characters(text)
    text = remove_stopwords_and_lemmatization(text)
    return text

def review(request, pk):
    if(request.session.has_key('account_id')):
        if(request.session['account_role'] == 2):
            content = {}
            movie = Movie.objects.get(pk = pk)
            content['title'] = 'Review ' + movie.name
            content['movie'] = movie
            content['my_review'] = ''
            checkReview = Review.objects.filter(critic = int(request.session['account_id']), movie = pk).first()
            if(checkReview):
                content['my_review'] = checkReview.review
                
            if(request.method == 'POST'):
                pass
            return render(request, 'critic/review.html', content)
        else:
            return HttpResponseForbidden()
    else:
        return HttpResponseRedirect(reverse('account-login'))
