from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$',views.admin_page,name="adminPage"),
    url(r'^user/delete/(\d+)$', views.delete_user),
    url(r'^gameProducts/$',views.gameProductList,name = 'gameProductList'),
    url(r'^gameProductDetail/(\d+)$',views.gameProductDetail,name = 'adminGameDetail'),
]