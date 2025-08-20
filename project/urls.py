from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

app_name = 'recipes'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('recipes.urls')),
    path('authors/', include('authors.urls')) # / primeiro elemento seria a pagina home da nossa aplicação.

]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
