from django.shortcuts import render, get_list_or_404, get_object_or_404
from utils.recipes.factory import make_recipe
from recipes.models import Recipe
from django.http import Http404

# Create your views here.

def home(request):
    recipes = Recipe.objects.filter(is_published=True).order_by('-id')
    #recipes = get_list_or_404(Recipe.objects.filter(is_published=True).order_by('-id'))
    return render(request, 'recipes/pages/home.html', context={'recipes':recipes})

def category(request, category_id):
    recipes = get_list_or_404(Recipe.objects.filter(category__id=category_id, is_published=True).order_by('-id'))
    return render(request, 'recipes/pages/category.html', context={'recipes':recipes, 'title': f'{recipes[0].category} - Category | Recipes'})


def recipe(request, id):
    recipe = get_object_or_404(Recipe, pk=id, is_published=True, )
    #recipe = Recipe.objects.filter(pk=id, is_published=True).order_by('-id').first() # Forma manual
    return render(request, 'recipes/pages/recipe-view.html', context={'recipe':recipe, 'is_detail_page':True})