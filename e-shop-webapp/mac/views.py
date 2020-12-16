from django.shortcuts import render

from math import ceil

# Create your views here.
from django.http import HttpResponse

def index(request):
    
    return render(request, 'index.html')
    


