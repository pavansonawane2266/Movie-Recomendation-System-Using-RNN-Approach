from pathlib import Path
from sys import path
from django.shortcuts import render
from itertools import count
from operator import imod
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords
import re
from joblib import dump, load
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.http import HttpResponseForbidden
from account.models import Profile, Role
from django.contrib import messages

BASE_DIR = Path(__file__).resolve().parent.parent

# Create your views here.
def index(request):
    if(request.session.has_key('account_id')):
        if(request.session['account_role'] == 1):
            content = {}
            content['title'] = 'Welcome Admin'
            return render(request, 'admin/index.html', content)
        else:
            return HttpResponseForbidden()
    else:
        return HttpResponseRedirect(reverse('account-login'))

def train_dataset(request):
    if(request.session.has_key('account_id')):
        if(request.session['account_role'] == 1):
            content = {}
            content['title'] = 'Train Dataset & Build Model'
            if(request.method == 'POST'):
                pass
            return render(request, 'admin/train_dataset.html', content)
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


def test_model(request):
    if(request.session.has_key('account_id')):
        if(request.session['account_role'] == 1):
            content = {}
            content['title'] = 'Train Dataset'
            return render(request, 'admin/test_dataset.html', content)
        else:
            return HttpResponseForbidden()
    else:
        return HttpResponseRedirect(reverse('account-login'))

def critics(request):
    if(request.session.has_key('account_id')):
        if(request.session['account_role'] == 1):
            content = {}
            content['title'] = 'Critics'
            content['critics'] = Profile.objects.filter(role_id = 2)
            return render(request, 'admin/critics.html', content)
        else:
            return HttpResponseForbidden()
    else:
        return HttpResponseRedirect(reverse('account-login'))

def criticsActivate(request, pk):
    if(request.session.has_key('account_id')):
        if(request.session['account_role'] == 1):
            if(request.method == "POST"):
                critic = Profile.objects.get(pk = pk)
                critic.status = 'Active'
                critic.save()
                messages.success(request, "Marked as active.")
                return HttpResponseRedirect(reverse('admin-critics'))
            else:
                messages.error(request, "Bad request.")
        else:
            return HttpResponseForbidden()
    else:
        return HttpResponseRedirect(reverse('account-login'))

def criticsInactive(request, pk):
    if(request.session.has_key('account_id')):
        if(request.session['account_role'] == 1):
            if(request.method == "POST"):
                critic = Profile.objects.get(pk = pk)
                critic.status = 'Inactive'
                critic.save()
                messages.success(request, "Marked as inactive.")
                return HttpResponseRedirect(reverse('admin-critics'))
            else:
                messages.error(request, "Bad request.")
        else:
            return HttpResponseForbidden()
    else:
        return HttpResponseRedirect(reverse('account-login'))
