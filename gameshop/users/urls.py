from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^login$',views.login, name='loginUser'),
    url(r'^logout$', views.logout, name='logoutUser'),
    url(r'^register$', views.registration, name='registerUser'),
]