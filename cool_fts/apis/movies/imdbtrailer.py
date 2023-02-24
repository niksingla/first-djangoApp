from django.http import HttpResponse, JsonResponse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from myprojects.models import trailerDB
from django.utils import timezone
import os
import validators
import requests
from my_site.settings import static_root


#import ast
#import platform
#print(os.environ.get('GOOGLE_CHROME_BIN'))
#print(platform.platform())
#print(STATIC_URL, STATIC_ROOT)
#print(os.environ.get("GOOGLE_CHROME_BIN"))

def flaskTrailer(imdb):
    print('Getting trailer from Flask API')
    url = 'https://imdb-trailer-api.herokuapp.com/'+imdb
    try:
        r= requests.get(url)
        trailer = r.json()
        if 'url' in trailer:
            trailer = trailer['url']
            print('Trailer fetch success')
            return trailer
        print('Trailer fetch failed')
        return 'Failed'
    except Exception as e:
        try:
            print(e)
            return getTrailer(imdb)
        except Exception as e:
            print(e)
            print('Something Went Wrong...')
            return 'Failed'

def trailerisValid(url):
    if validators.url(url)==True:
        return True
    else:
        return False
def getTrailer(imdb):
    print('Trailer API request made...')
    option = webdriver.ChromeOptions()
    if not os.environ.get("GOOGLE_CHROME_BIN")== None:
        option.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    option.add_argument('--headless')
    option.add_argument('--no-sandbox')
    option.add_argument('--disable-dev-shm-usage')
    option.add_argument('--log-level=3')
    if not os.environ.get('CHROMEDRIVER_PATH') == None:
        ex = os.environ.get('CHROMEDRIVER_PATH')
    else:
        ex = static_root+"\\cool_fts\\chromedriver.exe"
    try:
        driver = webdriver.Chrome(executable_path=ex,options=option)
        url = 'https://www.imdb.com/title/' + imdb
        driver.get(url)
        WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "video.jw-video.jw-reset")))
        videoElement = driver.find_element(By.CSS_SELECTOR, "video.jw-video.jw-reset")
        trailer = videoElement.get_attribute('src')
        if trailerisValid(trailer):
            return trailer
        print('something went wrong while fetching the trailer')
        return 'Failed'
    except Exception as e:
        #err= str(e)
        #return err +'\n '+ STATIC_ROOT + '\n' + platform.platform() + '\n' + str(os.environ.get("GOOGLE_CHROME_BIN"))+ '\n' + str(os.environ.get('CHROMEDRIVER_PATH'))
        print(e)
        return 'Failed'

def trailerExistReturn(imdbID, title):
    print('Checking trailer existance for: ',title)
    s = trailerDB.objects.filter(imdbID=imdbID).exists()
    if s:
        lastUpdated = (trailerDB.objects.get(imdbID=imdbID)).updatedOn
        if (timezone.now()-lastUpdated).days >=1:
            print('Updating trailer link...')
            trailer = flaskTrailer(imdbID)
            if trailer == 'Failed':
                return HttpResponse('Failed')
            currentTrailer = trailerDB.objects.filter(imdbID=imdbID)
            currentTrailer.update(trailer= trailer,updatedOn=timezone.now())
            trailerExistReturn(imdbID,title)
        #flaskTrailer(imdbID)
        trailer = (trailerDB.objects.get(imdbID=imdbID)).trailer
        return HttpResponse(trailer)
    else:
        trailer = flaskTrailer(imdbID)
        if not trailer == 'Failed':
            ins = trailerDB(title=title, updatedOn=timezone.now(), trailer=trailer, imdbID=imdbID)
            ins.save()
        return HttpResponse(trailer)

def trailerAPI(request):
    if(request.method=='POST'):
        imdbID = request.POST['id']
        title = request.POST['title']
        return trailerExistReturn(imdbID, title)
    else:
        return JsonResponse({'request':'failed'})