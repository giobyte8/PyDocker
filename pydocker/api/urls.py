from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^/container/start', views.start_container, name='container_start'),
    url(r'^/container/stop', views.stop_container, name='container_stop'),
]