from django.urls import path
from . import views

app_name = 'recipes'  

urlpatterns = [
    path('', views.RecipeListViewHome.as_view(), name='home'),  # <- isso cria a rota 'recipes:home'
    path('recipes/search/', views.RecipeListViewSearch.as_view(), name='search'),
    path('recipe/<int:pk>/', views.RecipeDetail.as_view(), name='recipe'),
    path('category/<int:category_id>/', views.RecipeListViewCategory.as_view(), name='category'),
    
]