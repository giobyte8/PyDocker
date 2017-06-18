from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^/$', views.index, name='index'),
    url(r'^/containers$', views.containers_grid, name='containers'),
    url(
        r'^/containers/details$',
        views.container_details,
        name='container_details'
    )
]