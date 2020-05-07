from django.shortcuts import render, get_object_or_404, reverse, HttpResponseRedirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import Recipe, Author
from .forms import RecipeAddForm, AuthorAddForm, LoginForm


def login_view(request):
    html = "generic_form.html"
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request, username=data['username'], password=data['password'])
            if user:
                login(request, user)

                return HttpResponseRedirect(request.GET.get('next', reverse("recipes:index")))
    return render(request, html, {'form': form})


@login_required()
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("recipes:index"))


def index(request):
    imageSrc = "https://images.unsplash.com/photo-1496262967815-132206202600?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9" \
               "&auto=format&fit=crop&w=2295&q=80 "
    recipes = Recipe.objects.all()
    return render(request, 'recipe/home.html', {'recipes': recipes, 'imageSrc': imageSrc})


def recipe_detail(request, recipe_id):
    imageSrc = "https://images.unsplash.com/photo-1496262967815-132206202600?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9" \
               "&auto=format&fit=crop&w=2295&q=80 "
    html = 'recipe/recipeDetail.html'
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    return render(request, html, {'recipe': recipe, 'imageSrc': imageSrc})


def author_detail(request, author_id):
    author = get_object_or_404(Author, pk=author_id)
    recipes = Recipe.objects.all()
    return render(request, 'recipe/authorDetail.html', {
        'author': author,
        'recipes': recipes,
    })


@login_required()
def add_author_view(request):
    html = "generic_form.html"
    form = AuthorAddForm()
    if request.method == "POST":
        form = AuthorAddForm(request.POST)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect(reverse("recipes:index"))

    return render(request, html, {'form': form})


@login_required()
def add_recipe_view(request):
    html = "generic_form.html"
    form = RecipeAddForm()
    if request.method == "POST":
        form = RecipeAddForm(request.POST)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect(reverse("recipes:index"))

    return render(request, html, {'form': form})


@login_required()
def delete_recipe(request, recipe_id):
    html = "recipe/recipeDelete.html"
    recipe_to_delete = get_object_or_404(Recipe, id=recipe_id)
    if request.method == "POST":
        recipe_to_delete.delete()
        return HttpResponseRedirect(reverse("recipes:index"))

    return render(request, html)


@login_required()
def update_recipe(request, recipe_id):
    html = "generic_form.html"
    recipe = Recipe.objects.get(id=recipe_id)

    form = RecipeAddForm(instance=recipe)
    if request.method == "POST":
        form = RecipeAddForm(request.POST, instance=recipe)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect(reverse("recipes:index"))
    return render(request, html, {'form': form})
