"""gameshop URL Configuration

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
from django.conf.urls import url, include
from django.conf import settings
from django.contrib import admin
from users.views import login
from django.views.static import serve

urlpatterns = [
    url(r'^',include('pages.urls')),
    url(r'^migrate/',include('migrate.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^users/login', login, name = "userLogin"),
    url(r'^users/logout', login, name="userLogout"),

]

# костыль для работы с media так и не понял ничего про static_root и перенос из медиа на продакшене
if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns.append(url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}))
