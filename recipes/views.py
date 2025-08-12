from django.shortcuts import render, get_list_or_404, get_object_or_404
from utils.recipes.factory import make_recipe
from recipes.models import Recipe
from django.http import Http404
from django.db.models import Q
import unicodedata

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

#def search(request):
#    search_term = request.GET.get('q', '').strip()

#    if not search_term:
#        raise Http404()
    
#    recipes = Recipe.objects.filter(
#        Q(
#            Q(title__icontains=search_term) |
#            Q(description__icontains=search_term)),
#        is_published=True
#    ).order_by('-id')

#    return render(request, 'recipes/pages/search.html', {
#        'page_title': f'Search for "{search_term}" |',
#       'search_term': search_term,
#        'recipes': recipes,
#    })

def normalize(text):
    return ''.join(
        c for c in unicodedata.normalize('NFKD', text)
        if not unicodedata.combining(c)
    ).lower()

def search(request):
    search_term = request.GET.get('q', '').strip()
    if not search_term:
        raise Http404()

    normalized_term = normalize(search_term)

    recipes = [
        r for r in Recipe.objects.filter(is_published=True)
        if normalized_term in normalize(r.title) or normalized_term in normalize(r.description)
    ]

    return render(request, 'recipes/pages/search.html', {
        'page_title': f'Search for "{search_term}" |',
        'search_term': search_term,
        'recipes': recipes,
    })
