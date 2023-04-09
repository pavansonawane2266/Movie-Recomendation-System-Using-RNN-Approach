from operator import mod
from django.db import models

# Create your models here.
class Role(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'roles'

class Profile(models.Model):
    username = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=70)
    password = models.CharField(max_length=20)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, default='Inactive')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'profiles'
