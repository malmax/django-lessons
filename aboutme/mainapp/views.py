from django.shortcuts import render, render_to_response
<<<<<<< HEAD
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
=======
from mainapp.models import getMainMenu, getAboutMeInfo, Works, Hobby, Learns
import logging
consolelog = logging.getLogger("console")

# Create your views here.
def showAboutPage(request):
    data = {"title":"Страница обо мне", "menu": getMainMenu(request.path)}
    data.update(getAboutMeInfo())
    data.update({'hobby' : map(lambda obj: obj,list(Hobby.objects.all()))})
    return render_to_response('about.html', data)

def showStudyPage(request):
    data = {"title":"Учеба", "menu": getMainMenu(request.path)}
    data.update(getAboutMeInfo())
    data.update({'learn': list(Learns.objects.all())})
    return render_to_response('learn.html',data)

def showWorkPage(request):
    data = {"title":"Работа", "menu": getMainMenu(request.path)}
    data.update(getAboutMeInfo())

    data.update({'works': list(Works.objects.all())})

    return render_to_response('work.html',data)

>>>>>>> 5b9e6c0b0a4570be83cea3b8d7da2f3a2ec53d6f
