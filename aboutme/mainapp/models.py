import logging
from django.urls import reverse
from datetime import date

from django.db import models

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
    # data['hobby'] = ['Большой теннис', 'Лыжи', 'Программирование']
    data['likeFilm'] = ['Форест Гамп']

    return data

class Organization(models.Model):
    title = models.CharField(max_length=100, unique=True, db_index=True)

    def __str__(self):
        return self.title

class Works(models.Model):
    organization = models.ForeignKey(Organization, null=True)
    employerName = models.CharField(max_length=30)
    startDate = models.DateField()
    title = models.CharField(max_length=30)

    def __str__(self):
        return self.employerName

class Learns(models.Model):
    imgName = models.CharField(max_length=30)
    shortTitle = models.CharField(max_length=50)
    longTitle = models.TextField()
    website = models.URLField(blank=True)

class Hobby(models.Model):
    title = models.CharField(max_length=40)

    def __str__(self):
        return self.title

