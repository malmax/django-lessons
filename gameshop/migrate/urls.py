from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^import/$',views.showImport),
]