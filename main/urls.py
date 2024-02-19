from django.urls import path
from django.conf.urls import url

from photoGraph import views


# app_name = ''

urlpatterns = [
    path('', views.index, name='index'),
]