from django.shortcuts import render
from django.contrib.auth.models import User
from django.views.generic import CreateView
from django.contrib.auth import logout

# Create your views here.

def index(request):
    return render(request, "index.html")

def logout (request):
    logout(request)