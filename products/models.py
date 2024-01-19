from django.db import models

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=50)
    content = models.TextField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    image = models.ImageField(upload_to='photos/%y/%m/%d')
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Phone'
        ordering = ['name']