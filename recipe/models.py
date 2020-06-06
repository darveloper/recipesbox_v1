from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.


class Author(models.Model):
    name = models.CharField(max_length=30)
    bio = models.TextField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    favorites = models.ManyToManyField('Recipe', related_name='favorites')
    
    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey('Author', on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.TextField()
    time_required = models.CharField(max_length=30)
    instructions = models.TextField(default="Instruction coming soon.")
    imageUrl = models.TextField(default='https://d2ebzu6go672f3.cloudfront.net/media/content/images'
                                        '/p3_MedDiet_W1806_gi667751254.jpg')
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title
