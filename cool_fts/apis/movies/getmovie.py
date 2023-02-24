from urllib import response
from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
from random import randint
from django.http import JsonResponse

def get_json_data(request):
    context = {}
    req = request.GET

    headers= {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36 Edg/102.0.1245.33"}
    if "genre" in req:
        bool_for_movie = not "tvshow" in req
        bool_for_tvshow = "tvshow" in req
        bool_for_rating_check = "rating" in req
        genre = request.GET.get("genre")
        if bool_for_movie:
            url = f"https://www.rottentomatoes.com/browse/movies_at_home/genres:{genre}~sort:popular?page=1"
            if genre == "":
                url = "https://www.rottentomatoes.com/browse/movies_at_home/sort:popular?page=1"
        else:
            url = f"https://www.rottentomatoes.com/browse/tv_series_browse/genres:{genre}~sort:popular?page=1"
            if genre == "":
                url = "https://www.rottentomatoes.com/browse/tv_series_browse/?page=1"
        title_list = []
        links_list = []
        imgs_list = []
        if bool_for_movie: #If request is for movies suggestion
            try: #Trying to map data
                response = requests.get(url, headers=headers)
                soup = BeautifulSoup(response.content, 'html.parser')
                data = soup.find('div', class_='discovery-grids-container')
                images = data.find_all('img', class_="js-lazyLoad")
                movies = data.find_all('span', class_='p--small')
                linkss = data.find_all('a')
                for image in images:
                    imgs_list.append(image.attrs['data-src'])    
                for movie in movies:
                    title_list.append(movie.text.strip())
                i = randint(0,len(title_list))
                title = title_list[i]   
                for link in linkss:
                        links_list.append("https://www.rottentomatoes.com"+link.attrs['href'])
                img = imgs_list[i]
                der =title_list[i].replace(" ","+")
                google_link = f"https://www.google.com/search?q={der}+movie"
                #--For getting OTT platform for the movie
                ur = links_list[i]
                r = requests.get(ur, headers=headers)
                soup1 = BeautifulSoup(r.content, 'html.parser')
                ott = []
                for o in soup1.find_all('where-to-watch-bubble'):
                    ott.append(o.attrs['image'])
                #--For getting genres of the movie----
                g= soup1.find('div', class_ ='meta-value genre')
                tmp = g.text.strip().replace('\n', "")
                tmp = tmp.replace(" & ", "$").replace(" ", "").replace("$", " & ").replace(",", ", ")
                
                tm = soup1.find('ul', class_="content-meta info").find_all('li', class_="meta-row clearfix")
                for it in tm:
                    temp = it.find('div', class_='meta-label subtle').text
                    if "Runtime" in temp:
                        runtime = it.find('time').text.strip()
                    elif "Release Date" in temp:
                        release = it.find('time').text.strip()
                context.update({"movie":title, "poster":img, "google_link":google_link})
                context.update({"ott":ott, "genres":tmp, "runtime":runtime, "releaseDate":release})
            except: #Backup for failure
                try:
                    base_url = "https://www.imdb.com"
                    url = f"https://www.imdb.com/search/title/?genres={genre}"
                    if genre == "":
                        url = "https://www.imdb.com/chart/moviemeter/"
                    
                    headers= {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36 Edg/102.0.1245.33"}
                    response = requests.get(url, headers=headers)
                    soup = BeautifulSoup(response.content, 'html.parser')
                    response = requests.get(url, headers=headers)
                    soup = BeautifulSoup(response.content, 'html.parser')
                    data = soup.find('div', id='main')
                    title_list = []
                    links_list = []
                    if genre!="":
                        titles = data.find_all('h3', class_='lister-item-header')
                    else:
                        titles = data.find_all('td', class_='titleColumn')
                    for item in titles:
                        title_list.append(item.find('a').text.strip())
                        link = base_url + (item.find('a').attrs['href']).split('?')[0]
                        links_list.append(link)
                    i = randint(0,len(titles))
                    title = title_list[i]
                    link = links_list[i]
                    dat = get_data(link)
                    poster = dat['poster']
                    genres = dat['genres']
                    release = dat['release']
                    runtime = dat['runtime']
                    der = title.replace(" ","+")
                    google_link = f"https://www.google.com/search?q={der}+movie"
                    context.update({"movie":title, "poster":poster, "google_link":google_link})
                    context.update({"ott":"", "genres":genres, "runtime":runtime, "releaseDate":release})
                except:
                    context = {'request':'failed'}
            
        elif bool_for_tvshow and (not bool_for_rating_check): #If request is for TV Show suggestion
            try: #Trying to map data
                response = requests.get(url, headers=headers)
                soup = BeautifulSoup(response.content, 'html.parser')
                data = soup.find('div', class_='discovery-grids-container')
                images = data.find_all('img', class_="js-lazyLoad")
                movies = data.find_all('span', class_='p--small')
                linkss = data.find_all('a')
                
                for image in images:
                    imgs_list.append(image.attrs['data-src'])    
                for movie in movies:
                    title_list.append(movie.text.strip())
                i = randint(0,len(title_list))
                title = title_list[i]
                for link in linkss:
                        links_list.append("https://www.rottentomatoes.com"+link.attrs['href'])
                ur = links_list[i]
                img = imgs_list[i]
                der =title_list[i].replace(" ","+")
                google_link = f"https://www.google.com/search?q={der}+series"
                #--For getting OTT platform for the TV Show
                r = requests.get(ur, headers=headers)
                soup1 = BeautifulSoup(r.content, 'html.parser')
                ott = []
                for o in soup1.find_all('where-to-watch-bubble'):
                    ott.append(o.attrs['image'])
                #--For getting genres of the TV Show----
                g= soup1.find('div', class_ ='col-right col-full-xs pull-right')
                tmp = g.find_all('tr')
                for item in tmp:
                    if "TV Network" in item.find('td', class_='fgm').text:
                        streamingOn = item.find_all('td')[1].text.strip()
                    elif "Premiere Date" in item.find('td', class_='fgm').text:
                        premDate = item.find_all('td')[1].text.strip()
                    elif "Genre:" in item.find('td', class_='fgm').text:
                        genres = item.find_all('td')[1].text.strip()
                context.update({"show":title, "poster":img, "google_link":google_link})
                context.update({"streamingOn":streamingOn, "genres":genres, "premDate":premDate, "ott":ott})
            except: #Backup for failure
                try:
                    response = requests.get(url, headers=headers)
                    soup = BeautifulSoup(response.content, 'html.parser')
                    base_url = "https://www.imdb.com"
                    url = f"https://www.imdb.com/search/title/?genres={genre}"
                    if genre == "":
                        url = "https://www.imdb.com/chart/tvmeter/"
                    headers= {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36 Edg/102.0.1245.33"}
                    response = requests.get(url, headers=headers)
                    soup = BeautifulSoup(response.content, 'html.parser')
                    data = soup.find('div', id='main')
                    title_list = []
                    links_list = []
                    if genre!="":
                        titles = data.find_all('h3', class_='lister-item-header')
                    else:
                        titles = data.find_all('td', class_='titleColumn')
                    for item in titles:
                        title_list.append(item.find('a').text.strip())
                        link = base_url + (item.find('a').attrs['href']).split('?')[0]
                        links_list.append(link)
                    i = randint(0,len(titles))
                    title = title_list[i]
                    link = links_list[i]
                    dat = get_data(link)
                    poster = dat['poster']
                    genres = dat['genres']
                    release = dat['release']
                    runtime = dat['runtime']
                    der = title.replace(" ","+")
                    google_link = f"https://www.google.com/search?q={der}+movie"
                    context.update({"show":title, "poster":poster, "google_link":google_link})
                    context.update({"ott":"", "genres":genres, "runtime":runtime, "releaseDate":release})
                    context.update({"streamingOn":"","premDate":""})
                except:
                    context = {'request':'failed'}
    elif "rating" in req:
        if not 'tvshow' in request.GET:
            context = get_rating(request, req, True)
        else:
            context = get_rating(request, req, False)
    return JsonResponse(context)
        
def get_rating(request, req, bool_for_movie):
    context = {}
    imdb = ''
    rt = ''
    q= request.GET.get("rating")
    if bool_for_movie:
        u = "https://www.google.com/search?q="+q+"movie"
    else:
        u = "https://www.google.com/search?q="+q.replace(" ", "+") +"+series"
    headers= {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36 Edg/102.0.1245.33"}
    r = requests.get(u, headers=headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    try:
        if bool_for_movie:        
            res = soup.find_all('a', class_='TZahnb vIUFYd')
            platforms = []
            
            if len(res)==0:
                context = {'imdb':'', 'rt':''}
            else:
                for item in res:
                    tmp = item.find('span', class_="rhsB pVA7K").attrs['title']
                    platforms.append(tmp)
                    if tmp == 'IMDb':
                        try:
                            imdb= item.find('span').text.strip()
                        except:
                            imdb = ""
                    elif tmp == 'Rotten Tomatoes':
                        try:
                            rt = item.find('span').text.strip()
                        except:
                            rt=''

                #print(platforms)
                if ('IMDb' in platforms) or ('Rotten Tomatoes' in platforms):            
                    context.update({"imdb":imdb, "rt":rt})
        else:
            res = soup.find('div', class_='zr7Aae aokhrd rVRkd')
            anchors = res.find_all('a')
            imdb = ""
            rt = ""
            if len(res)==0:
                context = {}
            else:
                for item in anchors:
                    tmp = item.find('span')                        
                    tmp2 = tmp.text.strip()
                    if "/" in tmp2:
                        imdb = tmp2
                    elif '%' in tmp2:
                        rt = tmp2
                context.update({"imdb":imdb, "rt":rt})

    except:
        context = {"rating-request":'failed'}

    return context
def get_data(link): #For IMdB only
    url = link
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36 Edg/102.0.1245.33"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')    
    poster = soup.find('meta', property='og:image').attrs['content']
    gen_info = (soup.find('div', {'class':'ipc-chip-list sc-16ede01-5 ggbGKe'})).find_all('li')
    release = (soup.find('section', {'data-testid':'Details'})).find('a', class_='ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link').text.strip()
    runtime = (soup.find('section', {'data-testid':'TechSpecs'})).find('div', class_='ipc-metadata-list-item__content-container').text.strip()
    genres= ""
    for item in gen_info:
        if genres=="":
            genres +=item.text.strip()
        else:
            genres += ', ' + item.text.strip()
    data = {'poster':poster, 'genres':genres, 'release':release, 'runtime':runtime}
    return data

#In development for fetching the list of data, change urls.py to use it
#"/apis/entertainment/?genre="
def data_list(request):
    context = {}
    req = request.GET
    genre = req.get('genre')
    title_list = []
    imgs_list = []
    links_list = []
    headers= {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36 Edg/102.0.1245.33"}
    if not ('tvshow' in req):
        if genre =='':
            url = 'https://www.rottentomatoes.com/browse/movies_at_home/sort:popular?page=1'
        else:
            url = f'https://www.rottentomatoes.com/browse/movies_at_home/genres:{genre}~sort:popular?page=1'
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        data = soup.find('div', class_='discovery-grids-container')
        images = data.find_all('img', class_="js-lazyLoad")
        movies = data.find_all('span', class_='p--small')
        linkss = data.find_all('a')
        for image in images:
            imgs_list.append(image.attrs['data-src'])    
        for movie in movies:
            title_list.append(movie.text.strip())
        for link in linkss:
                links_list.append("https://www.rottentomatoes.com"+link.attrs['href'])
        movies= []
        for i, v in enumerate(title_list):
            movies.append({'title': title_list[i], 'link':links_list[i], 'poster':imgs_list[i]})
        context.update({'result':movies, 'totalCount':len(movies)})
        
    else:
        if genre == "":
            url = "https://www.rottentomatoes.com/browse/tv_series_browse/?page=1"
        else:
            url = f"https://www.rottentomatoes.com/browse/tv_series_browse/genres:{genre}~sort:popular?page=1"
        
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        data = soup.find('div', class_='discovery-grids-container')
        images = data.find_all('img', class_="js-lazyLoad")
        movies = data.find_all('span', class_='p--small')
        linkss = data.find_all('a')    
        for image in images:
            imgs_list.append(image.attrs['data-src'])    
        for movie in movies:
            title_list.append(movie.text.strip())
        i = randint(0,len(title_list))
        title = title_list[i]
        for link in linkss:
            links_list.append("https://www.rottentomatoes.com"+link.attrs['href'])
        
        shows= []
        for i, v in enumerate(title_list):
            shows.append({'title': title_list[i], 'link':links_list[i], 'poster':imgs_list[i]})
        context.update({'result':shows, 'totalCount':len(shows)})
    
    #context.update({"movie":title_list, "poster":imgs_list, "google_link":"",'links':links_list, "totalResults":(len(title_list))})
    return JsonResponse(context)


#---this method is also working just make changes in the urls.py and unquote it---
"""def movie(request):
    
    context = {}
    if not "tvshow" in request.GET:
        if "genre" in request.GET:
            genre = request.GET.get("genre")
            url = f"https://www.rottentomatoes.com/browse/movies_at_home/genres:{genre}~sort:popular?page=1"
            if genre == "":
                url = "https://www.rottentomatoes.com/browse/movies_at_home/sort:popular?page=1"
            headers= {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36 Edg/102.0.1245.33"}
            try:
                response = requests.get(url, headers=headers)
                soup = BeautifulSoup(response.content, 'html.parser')
                data = soup.find('div', class_='discovery-grids-container')
                title_list = []
                links_list = []
                imgs_list = []
                images = data.find_all('img', class_="js-lazyLoad")
                movies = data.find_all('span', class_='p--small')
                linkss = data.find_all('a')
                
                for image in images:
                    imgs_list.append(image.attrs['data-src'])    
                for movie in movies:
                    title_list.append(movie.text.strip())
                i = randint(0,len(title_list))
                title = title_list[i]
                
                for link in linkss:
                        links_list.append("https://www.rottentomatoes.com"+link.attrs['href'])
                img = imgs_list[i]
                der =title_list[i].replace(" ","+")
                google_link = f"https://www.google.com/search?q={der}+movie"
                #--For getting OTT platform for the movie
                ur = links_list[i]
                r = requests.get(ur, headers=headers)
                soup1 = BeautifulSoup(r.content, 'html.parser')
                ott = []
                for o in soup1.find_all('where-to-watch-bubble'):
                    ott.append(o.attrs['image'])
                
                #--For getting genres of the movie----
                g= soup1.find('div', class_ ='meta-value genre')
                tmp = g.text.strip().replace('\n', "")
                tmp = tmp.replace(" & ", "$").replace(" ", "").replace("$", " & ").replace(",", ", ")
                
                tm = soup1.find('ul', class_="content-meta info").find_all('li', class_="meta-row clearfix")
                for it in tm:
                    temp = it.find('div', class_='meta-label subtle').text
                    if "Runtime" in temp:
                        runtime = it.find('time').text.strip()
                    elif "Release Date" in temp:
                        release = it.find('time').text.strip()

                
                context.update({"movie":title, "poster":img, "google_link":google_link})
                context.update({"ott":ott, "genres":tmp, "runtime":runtime, "releaseDate":release})
            #if above request gives error
            except:
                base_url = "https://www.imdb.com"
                url = f"https://www.imdb.com/search/title/?genres={genre}"
                if genre == "":
                    url = "https://www.imdb.com/chart/moviemeter/"
                headers= {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36 Edg/102.0.1245.33"}
                response = requests.get(url, headers=headers)
                soup = BeautifulSoup(response.content, 'html.parser')
                data = soup.find('div', id='main')
                title_list = []
                links_list = []
                if genre!="":
                    titles = data.find_all('h3', class_='lister-item-header')
                else:
                    titles = data.find_all('td', class_='titleColumn')
                for item in titles:
                    title_list.append(item.find('a').text.strip())
                    link = base_url + (item.find('a').attrs['href']).split('?')[0]
                    links_list.append(link)
                i = randint(0,len(titles))
                title = title_list[i]
                link = links_list[i]
                dat = get_data(link)
                poster = dat['poster']
                genres = dat['genres']
                release = dat['release']
                runtime = dat['runtime']
                der = title.replace(" ","+")
                google_link = f"https://www.google.com/search?q={der}+movie"
                context.update({"movie":title, "poster":poster, "google_link":google_link})
                context.update({"ott":"", "genres":genres, "runtime":runtime, "releaseDate":release})
                #context.update({"ott":ott, "genres":tmp, "runtime":runtime, "releaseDate":release})
            #print(context)
        elif "rating" in request.GET and not ("tvshow" in request.GET):
            q= request.GET.get("rating")
            u = "https://www.google.com/search?q="+q+"movie"
            headers= {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36 Edg/102.0.1245.33"}
            try:
                r = requests.get(u, headers=headers)
                soup = BeautifulSoup(r.content, 'html.parser')
                res = soup.find_all('a', class_='TZahnb vIUFYd')
                platforms = []
                
                if len(res)==0:
                    context = {}
                else:
                    
                    for item in res:
                        tmp = item.find('span', class_="rhsB pVA7K").attrs['title']
                        platforms.append(tmp)
                        if tmp == 'IMDb':
                            imdb= item.find('span').text.strip()
                        elif tmp == 'Rotten Tomatoes':
                            rt = item.find('span').text.strip()
                            

                    #print(platforms)
                    if ('IMDb' in platforms) or ('Rotten Tomatoes' in platforms):            
                        context.update({"imdb":imdb, "rt":rt})

            except:
                context = {}
            #print(context)
            return JsonResponse(context)
        else:
            context.update({"request":"failed"})    
        return JsonResponse(context)

#--------------GETTING DATA FOR TV SHOWS---------------

    elif "tvshow" in request.GET:
        if "genre" in request.GET:
            genre = request.GET.get("genre")
            url = f"https://www.rottentomatoes.com/browse/tv_series_browse/genres:{genre}~sort:popular?page=1"
            if genre == "":
                url = "https://www.rottentomatoes.com/browse/tv_series_browse/?page=1"
            headers= {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36 Edg/102.0.1245.33"}
            try:
                
                response = requests.get(url, headers=headers)
                soup = BeautifulSoup(response.content, 'html.parser')
                data = soup.find('div', class_='discovery-grids-container')
                title_list = []
                links_list = []
                imgs_list = []
                images = data.find_all('img', class_="js-lazyLoad")
                movies = data.find_all('span', class_='p--small')
                linkss = data.find_all('a')
                
                for image in images:
                    imgs_list.append(image.attrs['data-src'])    
                for movie in movies:
                    title_list.append(movie.text.strip())
                i = randint(0,len(title_list))
                title = title_list[i]
                
                for link in linkss:
                        links_list.append("https://www.rottentomatoes.com"+link.attrs['href'])
                ur = links_list[i]
                img = imgs_list[i]
                der =title_list[i].replace(" ","+")
                google_link = f"https://www.google.com/search?q={der}+series"
                
                
                #--For getting OTT platform for the TV Show
                
                r = requests.get(ur, headers=headers)
                soup1 = BeautifulSoup(r.content, 'html.parser')
                ott = []
                for o in soup1.find_all('where-to-watch-bubble'):
                    ott.append(o.attrs['image'])
                
                #--For getting genres of the TV Show----
                g= soup1.find('div', class_ ='col-right col-full-xs pull-right')
                tmp = g.find_all('tr')
                for item in tmp:
                    if "TV Network" in item.find('td', class_='fgm').text:
                        streamingOn = item.find_all('td')[1].text.strip()
                    elif "Premiere Date" in item.find('td', class_='fgm').text:
                        premDate = item.find_all('td')[1].text.strip()
                    elif "Genre:" in item.find('td', class_='fgm').text:
                        genres = item.find_all('td')[1].text.strip()
                context.update({"show":title, "poster":img, "google_link":google_link})
                context.update({"streamingOn":streamingOn, "genres":genres, "premDate":premDate, "ott":ott})
            except:
                base_url = "https://www.imdb.com"
                url = f"https://www.imdb.com/search/title/?genres={genre}"
                if genre == "":
                    url = "https://www.imdb.com/chart/tvmeter/"
                headers= {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36 Edg/102.0.1245.33"}
                response = requests.get(url, headers=headers)
                soup = BeautifulSoup(response.content, 'html.parser')
                data = soup.find('div', id='main')
                title_list = []
                links_list = []
                if genre!="":
                    titles = data.find_all('h3', class_='lister-item-header')
                else:
                    titles = data.find_all('td', class_='titleColumn')
                for item in titles:
                    title_list.append(item.find('a').text.strip())
                    link = base_url + (item.find('a').attrs['href']).split('?')[0]
                    links_list.append(link)
                i = randint(0,len(titles))
                title = title_list[i]
                link = links_list[i]
                dat = get_data(link)
                poster = dat['poster']
                genres = dat['genres']
                release = dat['release']
                runtime = dat['runtime']
                der = title.replace(" ","+")
                google_link = f"https://www.google.com/search?q={der}+movie"
                context.update({"show":title, "poster":poster, "google_link":google_link})
                context.update({"ott":"", "genres":genres, "runtime":runtime, "releaseDate":release})
                context.update({"streamingOn":"","premDate":""})
        elif "rating" in request.GET:
            
            q= request.GET.get("rating")
            u = "https://www.google.com/search?q="+q.replace(" ", "+") +"+series"
            headers= {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36 Edg/102.0.1245.33"}
            try:
                r = requests.get(u, headers=headers)
                
                soup = BeautifulSoup(r.content, 'html.parser')
                res = soup.find('div', class_='zr7Aae aokhrd rVRkd')
                anchors = res.find_all('a')
                imdb = ""
                rt = ""
                if len(res)==0:
                    context = {}
                else:
                    for item in anchors:
                        tmp = item.find('span')                        
                        tmp2 = tmp.text.strip()
                        if "/" in tmp2:
                            imdb = tmp2
                        elif '%' in tmp2:
                            rt = tmp2
                    context.update({"imdb":imdb, "rt":rt})

            except:
                context = {}
            #print(context)
        
            return JsonResponse(context)
        else:
            context.update({"request":"failed"})    
        return JsonResponse(context)
"""

