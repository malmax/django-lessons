from django.shortcuts import render, render_to_response

def index(request):
    name = "Maksim"
    return render_to_response('index.html', {'name': name})

# Create your views here.
