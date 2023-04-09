from operator import mod
from django.db import models
from account.models import Profile

# Create your models here.
class Movie(models.Model):
    name = models.CharField(max_length=50)
    released = models.DateField()
    year = models.IntegerField()
    sentiment = models.IntegerField(null=True)
    poster = models.ImageField(upload_to='movies/', blank=True)
    total_reviews = models.IntegerField(null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'movies_list'


class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    critic = models.ForeignKey(Profile, on_delete=models.CASCADE)
    review = models.TextField()
    sentiment = models.IntegerField(null=True)
    posted = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.review

    class Meta:
        db_table = 'reviews'
