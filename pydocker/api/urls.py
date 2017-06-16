from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^/containers/start', views.start_container, name='containers_start'),
    url(r'^/containers/stop', views.stop_container, name='containers_stop'),
]