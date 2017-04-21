from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^spots$', views.index, name='index'),
    url(r'^reserve/$', views.reserve, name='reserve')
]
