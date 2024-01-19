from django.shortcuts import render
from django.http import Http404, HttpResponse
from django.core.exceptions import *
from django.urls import *
# from .models import Product 

def index(request,id):
    try: 
        p = Product[id] 
    except : 
        raise Http404() 
    return render(request,'demoapp/index.html',{"Product":p})

Product=["apple","mhd"]