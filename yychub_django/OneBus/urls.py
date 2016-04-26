
from . import views
from django.conf.urls import url

urlpatterns = [
    url(r'^$', views.index),
    url(r'^api/route$', views.route_port),
    url(r'^api$', views.api_port),
]

