from django.db import models
from users.models import CustomUser
from datetime import date
class Book(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, unique=True)
    birthday = models.DateField()