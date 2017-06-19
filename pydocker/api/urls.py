from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^/container/start', views.container_start, name='container_start'),
    url(r'^/container/stop', views.container_stop, name='container_stop'),
]