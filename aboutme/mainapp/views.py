from django.shortcuts import render, render_to_response
from mainapp.models import getMainMenu, getAboutMeInfo
import logging
consolelog = logging.getLogger("console")

# Create your views here.
def showAboutPage(request):
    data = {"title":"Страница обо мне", "menu": getMainMenu(request.path)}
    data.update(getAboutMeInfo())
    return render_to_response('about.html', data)

def showStudyPage(request):
    data = {"title":"Учеба", "menu": getMainMenu(request.path)}
    data.update(getAboutMeInfo())
    return render_to_response('learn.html',data)

def showWorkPage(request):
    data = {"title":"Работа", "menu": getMainMenu(request.path)}
    data.update(getAboutMeInfo())
    return render_to_response('work.html',data)

