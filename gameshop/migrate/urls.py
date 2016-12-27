from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.showImport),
    url(r'^platforma/import', views.importPlatform),
    url(r'^platforma/del', views.importPlatformDel),
    url(r'^gameproduct/import', views.importGameProducts),
    url(r'^gameproduct/del', views.importGameProductsDel),
]