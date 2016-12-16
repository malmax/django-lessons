from django.shortcuts import render, render_to_response
from mainapp.models import getMainMenu
import logging

consolelog = logging.getLogger("console")


# Create your views here.
def showAboutPage(request):
    name = "максим"
    lastName = "малахов"
    middleName = "анатольевич"
    return render_to_response('about.html',
                              {"title": "Страница обо мне", "menu": getMainMenu(request.path), "name": name,
                               "lastName": lastName, "middleName": middleName})


def showStudyPage(request):
    return render_to_response('study.html', {"title": "Учеба", "menu": getMainMenu(request.path)})


def showWorkPage(request):
    workPlaces = [
        {'place': 'Место 1', 'post': 'PoSt 1', 'desc': 'Desctiption'},
        {'place': 'Место 2', 'post': 'PoSt 2', 'desc': 'Desctiption 2'},
        {'place': 'Место 3', 'post': 'PoSt 3', 'desc': 'Desctiption 3'}]


    return render_to_response('work.html',
                              {"title": "Работа", "menu": getMainMenu(request.path), "workPlaces": workPlaces})
