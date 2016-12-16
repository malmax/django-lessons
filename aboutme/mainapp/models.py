from django.db import models
from django.core.urlresolvers import reverse

import logging
consolelog = logging.getLogger("console")

# Create your models here.
def getMainMenu(url):
    # consolelog.debug(url)

    array = [{"text":"Главная","url": "home","active":False},
             {"text": "Учеба", "url": 'learn', "active": False},
             {"text": "Работа", "url": 'works', "active": False}]

    newArray = []
    for obj in array:
        if reverse(obj['url']) == url:
            obj['active'] = True
        newArray.append(obj)
    return newArray