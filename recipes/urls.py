from django.urls import path
from . import views


urlpatterns = [
    path('', views.home), #Home page
    path('recipes/<id>/', views.recipe), #Home page
]