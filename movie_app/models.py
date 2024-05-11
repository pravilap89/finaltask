from django.urls import reverse
from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=250, unique=True)
    slug = models.SlugField(max_length=250, unique=True)
    desc = models.TextField()

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def get_url(self):
        return reverse('movie:movieByCat', args=[self.slug])

    def __str__(self):
        return '{}'.format(self.name)




class Movie(models.Model):
    title = models.CharField(max_length=250)
    poster = models.ImageField(upload_to='media')
    description = models.CharField(max_length=250)
    release= models.DateField(auto_now=False)
    actors=models.TextField()
    trailer_link=models.CharField(max_length=300)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateField(auto_now=True)
    updated = models.DateField(auto_now=True)

    def __str__(self):
        return '{}'.format(self.title)

    def get_url(self):
        return  reverse('movie:movie_details',args=[self.id])


    class Meta:
        ordering = ('title',)
        verbose_name = 'movie'
        verbose_name_plural = 'movies'

class MovieRating(models.Model):
    comments=models.TextField()
    rating=models.IntegerField(max_length=10)
    movie=models.ForeignKey(Movie,on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now=True)

