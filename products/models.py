from django.db import models

# Create your models here.
class Product(models.Model):
    name=models.CharField(max_lenght=100)
    content=models.TextField()
    price=models.DecimalField(max_)