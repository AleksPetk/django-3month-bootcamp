from django.shortcuts import render, reverse
from django.http import HttpResponse
# Create your views here.

def home(request):
    return HttpResponse("It is working!")

