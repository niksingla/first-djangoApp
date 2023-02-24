from django.http import HttpResponse
from django.shortcuts import render
"""from django.shortcuts import render
from userid.google_tools import scrapper
from django.core.paginator import Paginator"""
from userid import models


#movies = scrapper.movies.movies()


def open_feature(request,features):
    if features == 'entertainment':
        return movie(request)
    elif features == 'music':
        return music(request)
    elif features == 'news':
        return news(request)
    elif features == 'sports':
        return sports(request)
    
def movie(request):
    context = {}
    if request.user.is_authenticated:
        current_user = request.user
        pic = models.UserProfile.objects.get(user=current_user).profile_pic
        
        context.update({"pic_url":pic})
    
    return render(request, 'movies/movies.html', context)

def music(request):
    return HttpResponse("MUSIC PAGE")
def news(request):
    return HttpResponse("NEWS PAGE")
def sports(request):
    return HttpResponse("SPORTS PAGE")
