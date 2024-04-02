from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Customized the default User model, so didn't change the name.
class User(AbstractUser):
    phone = models.CharField(max_length=11, blank=True, null=True)


class Movie(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name=models.CharField(max_length=255, blank=True, null=True)
    genre=models.CharField(max_length=255, blank=True, null=True)
    rating=models.CharField(max_length=255, blank=True, null=True)
    release_date=models.DateField(blank=True, null=True)

    def __str__(self):
        return self.name


class Ratings(models.Model):
    movie_id = models.ForeignKey(Movie, on_delete=models.CASCADE)
    rating = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return self.movie_id, self.rating