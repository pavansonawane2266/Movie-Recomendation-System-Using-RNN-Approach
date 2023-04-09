from django.contrib import messages
from movies.models import Movie
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.http import HttpResponseForbidden
# Create your views here.


def index(request):
    if(request.session.has_key('account_id')):
        if(request.session['account_role'] == 1):
            content = {}
            content['title'] = 'Movies'
            content['movies'] = Movie.objects.all().order_by('name')
            return render(request, 'admin/movies/index.html', content)
        else:
            return HttpResponseForbidden()
    else:
        return HttpResponseRedirect(reverse('account-login'))

def create(request):
    if(request.session.has_key('account_id')):
        if(request.session['account_role'] == 1):
            content = {}
            content['title'] = 'New Movie'
            if(request.method == 'POST'):
                movie = Movie()
                movie.name = request.POST['name'].title()
                movie.released = request.POST['date']
                movie.year = int(request.POST['year'])
                movie.poster = request.FILES['poster']
                movie.save()
                messages.success(request, "Movie added.")
                return HttpResponseRedirect(reverse('admin-movies-index'))
            return render(request, 'admin/movies/create.html', content)
        else:
            return HttpResponseForbidden()
    else:
        return HttpResponseRedirect(reverse('account-login'))
