from django.urls import path

from . import views

app_name = 'aigateway'
urlpatterns = [
    path('', views.home, name="home"),

]