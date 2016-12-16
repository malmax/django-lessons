"""aboutme URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from mainapp.views import showAboutPage
from mainapp.views import showStudyPage
from mainapp.views import showWorkPage

urlpatterns = [
    url(r'^admin/', admin.site.urls),
<<<<<<< HEAD
    url(r'^$', showAboutPage, name="home"),
    url(r'^learn/$', showStudyPage, name="learn"),
    url(r'^works/$', showWorkPage, name='works')
=======
    url(r'^$', showAboutPage, name = 'home'),
    url(r'^learn/$', showStudyPage, name = 'learn'),
    url(r'^work/$', showWorkPage,name = 'work')
>>>>>>> 5b9e6c0b0a4570be83cea3b8d7da2f3a2ec53d6f
]
