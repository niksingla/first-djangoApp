from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def projects(request):
    return render(request, 'projects/index.html')

def screen(request):
    return render(request, 'projects/screen.html')