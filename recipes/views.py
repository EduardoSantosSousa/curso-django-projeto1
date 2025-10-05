from django.shortcuts import render, get_list_or_404, get_object_or_404
from utils.recipes.factory import make_recipe
from recipes.models import Recipe
from django.http import Http404
from django.db.models import Q
import unicodedata
from utils.pagination import make_pagination
import os
from django.contrib import messages
from django.views.generic import ListView, DetailView
from django.http import JsonResponse
from django.forms.models import model_to_dict

PER_PAGE = int(os.environ.get('PER_PAGE', 6))

class RecipeListViewBase(ListView):
    model = Recipe
    context_object_name = 'recipes'
    ordering = ['-id']
    template_name = 'recipes/pages/home.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            is_published=True,
        )
        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        page_obj, pagination_range = make_pagination(
            self.request,
            ctx.get('recipes'),
            PER_PAGE
        )
        ctx.update(
            {'recipes': page_obj, 'pagination_range': pagination_range}
        )
        return ctx  


# Create your views here.

class RecipeListViewHome(RecipeListViewBase):
    template_name = 'recipes/pages/home.html'

class RecipeListViewHomeApi(RecipeListViewBase):
    template_name = 'recipes/pages/home.html'

    def render_to_response(self, context, **response_kwargs):
        recipes = self.get_context_data()['recipes']
        recipes_list = recipes.object_list.values() 

        return JsonResponse(list(recipes_list), safe=False)   

class RecipeListViewCategory(RecipeListViewBase):
    template_name = 'recipes/pages/category.html' 

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)   

        qs = qs.filter(category__id =self.kwargs.get('category_id'))

        if not qs:
            raise Http404()

        return qs
    

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        

        ctx.update({'title': f'{ctx.get("recipes")[0].category.name} - Category | Recipes'})

        return ctx

class RecipeListViewSearch(RecipeListViewBase):
    template_name = 'recipes/pages/search.html'

    def get_queryset(self, *args, **kwargs):
        search_term = self.request.GET.get('q', '')

        if not search_term:
            raise Http404()

        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            Q(
                Q(title__icontains=search_term) |
                Q(description__icontains=search_term),
            )
        )
        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        search_term = self.request.GET.get('q', '')

        ctx.update({
            'page_title': f'Search for "{search_term}" |',
            'search_term': search_term,
            'additional_url_query': f'&q={search_term}',
        })

        return ctx


def home(request):
    recipes = Recipe.objects.filter(is_published=True).order_by('-id')

    page_obj, pagination_range = make_pagination(request, recipes, PER_PAGE)

    return render(request, 'recipes/pages/home.html', context={
        'recipes':page_obj,
        'pagination_range':pagination_range
        })

def category(request, category_id):
    recipes = get_list_or_404(Recipe.objects.filter(category__id=category_id, is_published=True).order_by('-id'))

    page_obj, pagination_range = make_pagination(request, recipes, PER_PAGE)

    return render(request, 'recipes/pages/category.html', context={'recipes':page_obj,'pagination_range': pagination_range,
                                                                    'title': f'{recipes[0].category} - Category | Recipes'})


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
    
    messages.success(request, 'Epa, você foi pesquisar algo que eu vi.')
    
    search_term = request.GET.get('q', '').strip()
    if not search_term:
        raise Http404()

    normalized_term = normalize(search_term)

    recipes_qs = Recipe.objects.filter(is_published=True)
    recipes = [
        r for r in recipes_qs
        if normalized_term in normalize(r.title) or normalized_term in normalize(r.description)
    ]

    page_obj, pagination_range = make_pagination(request, recipes, PER_PAGE)

    return render(request, 'recipes/pages/search.html', {
        'page_title': f'Search for "{search_term}" |',
        'search_term': search_term,
        'recipes': page_obj,  
        'pagination_range': pagination_range,
        'addition_url_query':f'&q={search_term}'
    })

class RecipeDetail(DetailView):
    model = Recipe
    context_object_name = 'recipe'
    template_name = 'recipes/pages/recipe-view.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(is_published = True)
        return qs

    def get_context_data(self, *args,**kwargs):
        ctx = super().get_context_data(*args, **kwargs)

        ctx.update({

          'is_detail_page':True

        })

        return ctx


class RecipeDetailAPI(RecipeDetail):
    
    def render_to_response(self, context, **response_kwargs):
        recipe = self.get_context_data()['recipe']
        recipe_dict = model_to_dict(recipe)

        recipe_dict['create_at'] = str(recipe.created_at)
        recipe_dict['updated_at'] = str(recipe.created_at)

        if recipe_dict.get('cover'):
            recipe_dict['cover'] = self.request.build_absolute_uri() + recipe_dict['cover'].url[1:]
        else:
             recipe_dict['cover'] = ''  

        del recipe_dict['is_published']
        del recipe_dict['preparation_steps_is_html']      

        return JsonResponse(recipe_dict, safe=False)
    