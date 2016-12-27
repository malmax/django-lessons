from django.shortcuts import render, Http404, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def loginForm():
    pass

def login(request):
    if request.method == 'POST':
        username = request.POST.get('login')
        password = request.POST.get('password')

        user = authenticate(username = username, password = password)
        if user:
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            return render(request, 'index.html', {'username': username, 'errors': True})

    raise Http404

def logout(request):
    HttpResponseRedirect('/')

def register(request):
    HttpResponseRedirect('/')