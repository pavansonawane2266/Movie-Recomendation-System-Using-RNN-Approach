from re import search
from movies.models import Movie, Review
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponseForbidden
from django.urls import reverse
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Create your views here.
def index(request):
	content = {}
	content['title'] = 'Movies'
	content['movies'] = Movie.objects.all().order_by('name')
	content['searckkey'] = ''
	if(request.method == 'POST'):
		serach_keyword = request.POST['search']
		content['searckkey'] = serach_keyword
		content['movies'] = Movie.objects.filter(name__icontains=serach_keyword).order_by('name')
	return render(request, 'home/index.html', content)

def reviews(request, pk):
	content = {}
	movie = Movie.objects.get(pk = pk)
	content['title'] = movie.name + ' reviews'
	reviews = Review.objects.filter(movie = pk)
	if(reviews.count() > 0):
		content['reviews'] = reviews
	else:
		content['reviews'] = None
	content['movies'] = movie
	return render(request, 'home/reviews.html', content)
	
