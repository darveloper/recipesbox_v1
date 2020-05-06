from django.urls import path
from . import views

app_name = 'recipes'

urlpatterns = [
    path('', views.index, name='index'),
    path('recipe/<int:recipe_id>/', views.recipe_detail, name="recipe_detail"),
    path('author/<int:author_id>/', views.author_detail, name="authorDetail")
]
