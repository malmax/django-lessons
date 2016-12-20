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
    data['likeFilm'] = ['Форест Гамп']

    return data

class Organization(models.Model):
    title = models.CharField(max_length=100, unique=True, db_index=True)
    region = models.CharField(max_length=50, blank=True)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=100)

    def __str__(self):
        return self.title

class Works(models.Model):
    organization = models.ForeignKey(Organization)
    startDate = models.DateField()
    endDate = models.DateField(blank=True, null=True)
    title = models.CharField(max_length=30, verbose_name="Должность")

    def __str__(self):
        return self.organization + " " + self.title

class Learns(models.Model):
    imgName = models.CharField(max_length=30)
    shortTitle = models.CharField(max_length=50)
    longTitle = models.TextField()
    website = models.URLField(blank=True)

class Hobby(models.Model):
    title = models.CharField(max_length=40)

    def __str__(self):
        return self.title

