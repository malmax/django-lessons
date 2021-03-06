from django.shortcuts import render, render_to_response
from mainapp.models import getMainMenu, getAboutMeInfo, Works, Hobby, Learns, Organization
import logging

consolelog = logging.getLogger("console")


# Create your views here.
def showAboutPage(request):
    data = {"title": "Страница обо мне", "menu": getMainMenu(request.path)}
    data.update(getAboutMeInfo())
    data.update({'hobby': map(lambda obj: obj, list(Hobby.objects.all()))})
    return render_to_response('about.html', data)


def showStudyPage(request):
    data = {"title": "Учеба", "menu": getMainMenu(request.path)}
    data.update(getAboutMeInfo())
    data.update({'learn': list(Learns.objects.all())})
    return render_to_response('learn.html', data)


def showWorkPage(request, lastWorkCheckbox = False):
    data = {"title": "Работа", "menu": getMainMenu(request.path)}
    data.update(getAboutMeInfo())

    if not lastWorkCheckbox:
        checked =  False
        data.update({'works': list(Works.objects.all())})
    else:
        checked =  True
        data.update({'works': list(Works.objects.all())[:3]})

    data.update({'lastWork': checked })

    return render_to_response('work.html', data)


def showOrganization(request, organizationId):
    data = {"title": "Информация об организации", "menu": getMainMenu(request.path)}
    data.update(getAboutMeInfo())
    data.update({"organization": Organization.objects.get(pk = organizationId)})

    return render_to_response('organization.html', data)
