from django.urls import path
from .views import site
from recipes import views

app_name = 'recipes'  

urlpatterns = [
    path('', site.RecipeListViewHome.as_view(), name='home'),  # <- isso cria a rota 'recipes:home'
    path('recipes/search/', site.RecipeListViewSearch.as_view(), name='search'),
    path('recipe/<int:pk>/', site.RecipeDetail.as_view(), name='recipe'),
    path('category/<int:category_id>/', site.RecipeListViewCategory.as_view(), name='category'),
    path('recipes/api/v1/', site.RecipeListViewHomeApi.as_view(), name='recipe_api_v1', ),
    path('recipes/api/v1/<int:pk>', site.RecipeDetailAPI.as_view(), name='recipe_api_v1_detail', ),
    path('recipes/theory/', site.theory, name='theory',),
    path('recipes/api/v2/', views.recipe_api_list, name='recipes_api_v2'),
    path('recipes/api/v2/<int:pk>/', views.recipe_api_detail, name='recipes_api_v2_detail'),
    
]