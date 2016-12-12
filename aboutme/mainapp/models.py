from django.db import models
import logging
from django.urls import reverse
from datetime import date

consolelog = logging.getLogger("console")


# Create your models here.
def getMainMenu(url="home"):
    # consolelog.debug(url)

    array = [{"text": "Главная", "urlName": "home", "active": False},
             {"text": "Учеба", "urlName": "learn", "active": False},
             {"text": "Работа", "urlName": "work", "active": False}]

    newArray = []
    for obj in array:
        if reverse(obj['urlName']) == url:
            obj['active'] = True
        newArray.append(obj)
    return newArray


def getAboutMeInfo():
    data = {}
    data['lastName'] = 'Малахов'
    data['firstName'] = 'Максим'
    data['thirdName'] = 'Анатольевич'
    data['birthday'] = date(1984, 5, 5)
    data['hobby'] = ['Большой теннис', 'Лыжи', 'Программирование']
    data['likeFilm'] = ['Форест Гамп']
    data['works'] = [{'employer': 'ООО \"Планета Игр\"', 'startDate':date(2010,6,1), 'title': 'Менеджер по работе с клиентами'},
                     {'employer': 'ООО \"НьюсФлай\"', 'startDate': date(2005,1,1), 'title': 'Менеджер по работе с клиентами'}]
    data['learn'] = [{'imgName':'school.gif', 'shortTitle': 'Школа №40', 'longTitle': 'Школа №40 Приморского р-на Санкт-Петербурга','website':'http://licey40.siteedit.ru/'},
                     {'imgName': 'univer.jpg', 'shortTitle': 'СПБГПУ', 'longTitle': 'Санкт-Петербургский Государственный Политехнический Университет','website':'http://www.spbstu.ru/'}]
    return data



