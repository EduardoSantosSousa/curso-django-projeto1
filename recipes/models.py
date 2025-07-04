from django.db import models
from django.contrib.auth.models import User
from PIL import Image  # <- IMPORTANTE!

class Category(models.Model):
    name = models.CharField(max_length=65)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    title = models.CharField(max_length=65)
    description = models.CharField(max_length=165)
    slug = models.SlugField()
    preparation_time = models.IntegerField()
    preparation_time_unit = models.CharField(max_length=65)
    servings = models.IntegerField()
    servings_unit = models.CharField(max_length=65)
    preparation_steps = models.TextField()
    preparation_steps_is_html = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    cover = models.ImageField(upload_to='recipes/covers/%Y/%m/%d', blank=True, default='')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, default=None)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Redimensionar imagem se existir
        if self.cover:
            try:
                img = Image.open(self.cover.path)

                # Define tamanho máximo (ajuste conforme necessário)
                max_width = 800
                max_height = 600

                if img.height > max_height or img.width > max_width:
                    img.thumbnail((max_width, max_height))
                    img.save(self.cover.path)
            except Exception as e:
                print(f"Erro ao redimensionar imagem: {e}")

    