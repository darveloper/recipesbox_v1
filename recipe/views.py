from django.shortcuts import render, get_object_or_404, reverse, HttpResponseRedirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import Group
from .decorators import unauthenticated_user, allowed_users
from recipe.models import Recipe, Author
from .forms import RecipeAddForm, AuthorAddForm, LoginForm, RegisterUserForm
from django.contrib.auth.models import User


@unauthenticated_user
def login_view(request):
    # html = "generic_form.html"
    html = "recipe/login.html"
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            username = form.cleaned_data.get('username')
            print('username', username)
            user = authenticate(request, username=data['username'], password=data['password'])
            if user:
                login(request, user)
                return HttpResponseRedirect(request.GET.get('next', reverse("recipes:index")))
            else:
                messages.error(request, 'Your email or Password is incorrect.')
    return render(request, html, {'form': form})


@unauthenticated_user
def register_view(request):
    # html = "generic_form.html"
    html = "recipe/register_user.html"
    form = RegisterUserForm()
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            print(username)


            return HttpResponseRedirect(reverse("recipes:login_page"))

    return render(request, html, {'form': form})


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
@allowed_users(allowed_roles=['admin'])
def add_author_view(request):
    # html = "generic_form.html"
    html = "recipe/addauthor.html"
    form = AuthorAddForm()
    if request.method == "POST":
        form = AuthorAddForm(request.POST)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect(reverse("recipes:index"))

    return render(request, html, {'form': form})


@login_required()
def add_recipe_view(request):
    # html = "generic_form.html"
    #
    html = "recipe/addrecipe.html"
    form = RecipeAddForm()
    if request.method == "POST":
        form = RecipeAddForm(request.POST)
        if form.is_valid():
            form.save()
            author = form.cleaned_data.get('description')
            print(author)
        return HttpResponseRedirect(reverse("recipes:index"))

    return render(request, html, {'form': form})


@login_required()
def delete_recipe(request, recipe_id):
    html = "recipe/recipeDelete.html"
    recipe_to_delete = get_object_or_404(Recipe, id=recipe_id)
    if request.method == "POST":
        recipe_to_delete.delete()
        return HttpResponseRedirect(reverse(" "))

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


#
@login_required()
@allowed_users(allowed_roles=['author'])
def userpage(request):
    html = "recipe/user_page.html"
    users = Author.objects.all()
    curr_user = User.objects.get(username=request.user)
    db_user = Author.objects.get(user=curr_user)
    recipe_users = Recipe.objects.filter(author=db_user)

    return render(request, html, {'user': users, 'recipe_users': recipe_users})


def accessdenied(request):
    html = "recipe/accessdenied.html"
    return render(request, html)

def add_favorite_view(request, id):
    current_user = Author.objects(name=request.user)
    recipe_to_faovrite = Recipe.objects.get(id=id)
    current_user.favorites.add(recipe_to_faovrite)
    current_user.save()
    return HttpResponseRedirect(reverse('home'))

def favorites_view(request, id):
    current_user = Author.objects.get(id=id)
    return render(request, 'favorites.html', {"favorites":current_user.favorites.all()})