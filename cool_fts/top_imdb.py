from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator
import requests
from bs4 import BeautifulSoup
from django.shortcuts import render, redirect
from userid import models

class movies:    
    def movies():
        
        req = requests.get("https://www.imdb.com/search/title/?count=100&groups=top_1000&sort=user_rating")


        soup = BeautifulSoup(req.content, 'html.parser')

        movie_data = soup.find_all('div', class_='lister-item mode-advanced')

        movies= []
        imdb = []
        count = 1
        for store in movie_data:
            name = store.h3.a.text
            tmp = (store.find('div', 'inline-block ratings-imdb-rating')).find('strong').text.strip()
            name = f"{count}. {name} ({tmp})"
            link = "https://www.imdb.com" + store.h3.a.attrs['href']
            movies.append({name:link})
            
            count += 1
        
        return movies
movList = movies.movies()
print("IMDB Imported")
def topImdb(request):
    movie_names = []
    movie_links = []
    
    movies_paginator = Paginator(movList, 10)
    page_num = request.GET.get('page')
    page = movies_paginator.get_page(page_num)
    count = int(len(movList)/10)
    
    for item in page.object_list:
        for k,v in item.items():
            movie_names.append(k)
            movie_links.append(v)
    
    context = {
        "page": page,
        "page_count": movies_paginator.page_range,
        "names_links":zip(movie_names, movie_links),
        "count": count,      
        }
    if request.user.is_authenticated:
        current_user = request.user
        pic = models.UserProfile.objects.get(user=current_user).profile_pic
        
        context.update({"pic_url":pic})
    
    return render(request, 'movies/top-imdb.html',context)