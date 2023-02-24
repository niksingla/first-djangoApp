from userid.google_tools import scrapper
from django.shortcuts import render
import datetime

def home_content_api(request):
    country = request.GET.get('country')
    print(country)
    now = datetime.datetime.now() 
    query= "latest"
    titles=[]
    links=[]
    times=[]
    descs=[]
    images=[]
    
    temp = scrapper.home_content.news_api(country)
    if not temp["title"] == "":
        titles = temp["title"]
        links= temp["link"]
        times = temp["time"]
        descs = temp["desc"]
        images = temp["image"]
            
    
    content={
        "titles":titles,
        "links":links,
        "times":times,
        "descs":descs,
        "images":images
        
    }     

    #content.update({"query":query})  
    content.update({"titles_links_times_descs_images": zip(titles,links,times,descs,images)})
    diff = datetime.datetime.now() - now
    print(diff.total_seconds())
    return render(request, "home-content.html", content)