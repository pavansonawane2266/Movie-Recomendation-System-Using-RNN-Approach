from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from account.models import Profile, Role
from django.db.models import Q
from django.contrib import messages

# Create your views here.
def insertRoles():
    roles = Role.objects.count()
    if(roles < 1):
        role = Role()
        role.name = 'Admin'
        role.save()
        role = Role()
        role.name = 'User'
        role.save()

def insertAdmin():
    admins = Profile.objects.count()
    if(admins < 1):
        admin = Profile()
        admin.name = 'Admin'
        admin.username = 'admin'
        admin.password = 'admin@123'
        admin.status = 'Active'
        admin.role = Role.objects.get(pk=1)
        admin.save()

def login(request):
    content = {}
    insertRoles()
    insertAdmin()
    if request.session.has_key('account_id'):
        if (request.session['account_role'] == 1):
            return HttpResponseRedirect(reverse('admin-index'))
        else:
            return HttpResponseRedirect(reverse('critic-index'))
    content['title'] = 'Login'
    if(request.method == 'POST'):
        username = request.POST['username']
        password = request.POST['password']
        profile = Profile.objects.filter(username = username, password = password).first()
        if(profile):
            if(profile.status == 'Active'):
                request.session['account_name'] = profile.name
                request.session['account_id'] = profile.id
                request.session['account_role'] = profile.role_id
                if(profile.role_id == 1):
                    return HttpResponseRedirect(reverse('admin-index'))
                else:
                    return HttpResponseRedirect(reverse('critic-index'))
            else:
                messages.error(request, "Your account is inactive.")    
        else:
            messages.error(request, "Credentials provided does not matched in our records.")
    return render(request, 'account/login.html', content)


def signup(request):
    content = {}
    # insertRoles()
    # insertAdmin()
    content['title'] = 'Sign up'
    if(request.method == 'POST'):
        username = request.POST['username']
        name = request.POST['name']
        password = request.POST['password']
        profile = Profile()
        profile.name = name.title()
        profile.username = username.lower()
        profile.password = password
        profile.role = Role.objects.get(pk=2)
        profile.status = 'Inactive'
        profile.save()
        return HttpResponseRedirect(reverse('account-login'))
    return render(request, 'account/signup.html', content)


def logout(request):
    del request.session['account_name']
    del request.session['account_id']
    del request.session['account_role']
    messages.success(request, "You are logged out!.")
    return HttpResponseRedirect(reverse('account-login'))
