from django.urls import path

from . import views

app_name = 'aigateway'
urlpatterns = [
    path('projects/', views.proj, name="proj"),
    path('models/', views.aimodel, name="models"),
    path('dataset/', views.dataset, name="dataset"),
]
