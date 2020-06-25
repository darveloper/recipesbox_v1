from django import forms
from .models import Author, Recipe
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RecipeAddForm(forms.ModelForm):

    class Meta:
        model = Recipe
        fields = ['author', 'title', 'description',
                  'time_required', 'instructions']

class RecipeEditForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'description', 'time_required', 'instructions']

class AuthorAddForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = '__all__'


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput)


class RegisterUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', ]
