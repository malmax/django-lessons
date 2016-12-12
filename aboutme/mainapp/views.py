from django.shortcuts import render, render_to_response
from mainapp.models import getMainMenu
import logging
consolelog = logging.getLogger("console")

# Create your views here.
def showAboutPage(request):
    return render_to_response('about.html',{"title":"Страница обо мне", "menu": getMainMenu(request.path)})

def showStudyPage(request):
    return render_to_response('study.html',{"title":"Учеба", "menu": getMainMenu(request.path)})

def showWorkPage(request):
    # consolelog.debug(
    #     msg=request)
    return render_to_response('work.html',{"title":"Работа", "menu": getMainMenu(request.path)})

