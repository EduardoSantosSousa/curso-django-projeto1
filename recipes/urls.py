from django.urls import path
from . import views

app_name = 'recipes'  

urlpatterns = [
    path('', views.home, name='home'),  # <- isso cria a rota 'recipes:home'
    path('recipes/search/', views.search, name='search'),
    path('recipe/<int:id>/', views.recipe, name='recipe'),
    path('category/<int:category_id>/', views.category, name='category'),
    
]