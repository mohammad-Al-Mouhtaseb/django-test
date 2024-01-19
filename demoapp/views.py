from django.shortcuts import render
from django.http import Http404, HttpResponse
from django.core.exceptions import *
from django.urls import *
# from .models import Product 

def index(request):
    return render(request,'demoapp/index.html',{"text":"index"})

def about(request):
    return render(request,'demoapp/about.html',{"text":"about"})