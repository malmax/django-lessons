from django.db import models
import logging
consolelog = logging.getLogger("console")

# Create your models here.
def getMainMenu(url):
    consolelog.debug(url)

    array = [{"text":"Главная","url":"/","active":False},
             {"text": "Учеба", "url": "/study/", "active": False},
             {"text": "Работа", "url": "/work/", "active": False}]

    newArray = []
    for obj in array:
        if obj['url'] == url:
            obj['active'] = True
        newArray.append(obj)
    return newArray