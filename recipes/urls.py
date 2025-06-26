from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name="recipes-home"), #Home page
    path('recipes/<id>/', views.recipe, name="recipes-recipe"), #Home page
]