from django.shortcuts import render
from . models import *

# Create your views here.
def products(request):
    return render(request,'products/products.html',{"product":Product.objects.all()})

def product(request):
    return render(request,'products/product.html',{"product":Product})

