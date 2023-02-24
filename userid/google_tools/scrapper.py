from random import random
from requests_html import HTMLSession
import requests 
from bs4 import BeautifulSoup
from lxml import etree
import random
import datetime, pytz
import environ

env = environ.Env()
environ.Env.read_env()
#print(env('NEWS_API_KEY'))


class weather:
    def get_weather(query):    
        session = HTMLSession()

        query = query

        url= f'https://www.google.com/search?q=weather+{query}'

        r = session.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36 Edg/99.0.1150.46'})

        soup = BeautifulSoup(r.content, 'html.parser')
        dom = etree.HTML(str(soup))
        try:
            clouds = (dom.xpath('//*[@id="wob_dc"]'))[0].text
            temperature = (dom.xpath('//*[@id="wob_tm"]'))[0].text
        except:
            clouds= "Enter Valid Location"
        
        
        print(clouds, temperature+" degrees")
        return clouds
        
#https://www.google.com/search?q=movies&source=lnms&tbm=nws&sa=X&ved=2ahUKEwjk1MWz1-T2AhUJwzgGHRdRBPQQ_AUoA3oECAIQBQ&biw=1536&bih=754&dpr=1.25
class home_content:

    def gnews_api(query):
        
        query = query
        session = HTMLSession() 
        token= env('GNEWS_TOKEN')
        url= f"https://gnews.io/api/v4/top-headlines?&token={token}&lang=en&country=in"
    
        r = session.get(url)
        json_data = r.json()["articles"]
        
        count = len(json_data)
        
        #index = random.randint(1,count)
        titles = []
        urls = []
        images = []
        times = []
        descs = []
        formatted_times = []
        
        for items in json_data:
            titles.append(items["title"])
            urls.append(items["url"])
            images.append(items["image"])
            descs.append(items["description"])
            times.append(items["publishedAt"])
        now = str(datetime.datetime.now(pytz.timezone('UTC'))).split('.')[0]
        now = datetime.datetime.strptime(now, '%Y-%m-%d %H:%M:%S')      
        for tim in times:
            try:
                art_time = str(tim).replace('T', ' ').replace('Z', ' ').strip()
                art_time = datetime.datetime.strptime(art_time, '%Y-%m-%d %H:%M:%S')
                
                diff = now - art_time
                diff = int(diff.total_seconds())
                
                if diff>59 and diff<3601:
                    diff = f"{int(diff/60)} mins ago"
                elif diff<61:
                    diff = f"{int(diff)} secs ago"
                elif diff>3599 and diff<86400:
                    diff = f"{int(diff/60/60)} hours ago"
                elif diff>86399:
                    diff = f"{int(diff/24/60/60)} days ago"
                formatted_times.append(diff)

            except:
                formatted_times.append('')
        content = {"title":titles,"link":urls,"time":formatted_times,"desc":descs, "image":images}
        return content  
        
    def news_api(query):     
        query = query
        session = HTMLSession() 
        api_key = env('NEWS_API_KEY')
        url= f"https://newsapi.org/v2/top-headlines?country={query}&sortBy=publishedAt&apiKey={api_key}&language=en"
        try:
            r = session.get(url)    
            json_data = r.json()["articles"]
            count = len(json_data)
            
            index = random.randint(1,int(count/2))
            titles = []
            urls = []
            images = []
            times = []
            descs = []
            formatted_times = []

            for items in json_data:
                titles.append(items["title"])
                urls.append(items["url"])
                images.append(items["urlToImage"])
                descs.append(items["description"])
                times.append(items["publishedAt"])
            
            now = str(datetime.datetime.now(pytz.timezone('UTC'))).split('.')[0]
            now = datetime.datetime.strptime(now, '%Y-%m-%d %H:%M:%S')      
            
            for tim in times:
                try:
                    art_time = str(tim).replace('T', ' ').replace('Z', ' ').strip()
                    art_time = datetime.datetime.strptime(art_time, '%Y-%m-%d %H:%M:%S')
                    
                    diff = now - art_time
                    diff = int(diff.total_seconds())
                    
                    if diff>59 and diff<3601:
                        formatted_times.append(f"{int(diff/60)} mins ago")
                    elif diff<61:
                        formatted_times.append(f"{int(diff)} secs ago")
                    elif diff>3599 and diff<86400:
                        formatted_times.append(f"{int(diff/60/60)} hours ago")
                    elif diff>86399:
                        formatted_times.append(f"{int(diff/24/60/60)} days ago")
                except:
                    formatted_times.append("")
            #now_utc = str(now.astimezone(pytz.utc)).split("+")[0]
            content = {"title":titles,"link":urls,"time":formatted_times,"desc":descs, "image":images}
            return content  

        except:
            
            try:
                return home_content.gnews_api(query)
            except:
                return home_content.get_content(query)
          
    def get_content(query):
        
        """session = HTMLSession()
        query = query"""
        
        url= f"https://www.google.com/search?q=news&tbm=nws" 
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36 Edg/99.0.1150.46'}
        try:
            req= requests.get(url, headers=headers)
            soup = BeautifulSoup(req.content, 'html.parser')
            
            blocks = soup.find_all('g-card', class_='ftSUBd')
            titles = []
            descs = []
            links = []
            times = []
            images = []
            for t in blocks:
                titles.append(t.find('div', role='heading').text.replace('\n', '').strip())    
                descs.append(t.find('div', class_='GI74Re nDgy9d').text.strip())
                ln = t.find('a').attrs['href']
                links.append(ln)
                times.append(t.find('div', class_='OSrXXb ZE0LJd').find('span').text.strip())
                images.append(home_content.get_image(ln))

            print(len(blocks))
            print(images[0])
            
            
            #Getting content using DOM, etree
            """dom = etree.HTML(str(soup))

            count= len((dom.xpath(f'//*[@id="rso"]/div/g-card/div/div/a/div/div[2]/div[2]')))
            index = random.randint(0, count)
            
            
            try:
                content_title = (dom.xpath(f'//*[@id="rso"]/div[{index}]/g-card/div/div/a/div/div[2]/div[2]'))[0].text            
            except:
                content = {"title":"","link":"","time":"","desc":"", "image":""}
                return content
                
            
            try:
                content_link = (dom.xpath(f'//*[@id="rso"]/div[{index}]/g-card/div/div/a'))[0].attrib['href']
            except:
                content_link = "#"
            
            try:
                content_time = (dom.xpath(f'//*[@id="rso"]/div[{index}]/g-card/div/div/a/div/div[2]/div[4]/span'))[0].text
            
            except:
                content_time = "####"    
            
            try:
                content_desc = (dom.xpath(f'//*[@id="rso"]/div[{index}]/g-card/div/div/a/div/div[2]/div[3]'))[0].text
            except:
                content_desc = "Something went wrong"
            
            try:        
                content_image = home_content.get_image(content_link)
            except:
                content_image = "No Image Found"
            
            content = {"title":content_title,"link":content_link,"time":content_time,"desc":content_desc, "image":content_image}
            """
            
            content = {"title":titles,"link":links,"time":times,"desc":descs, "image":images}
        except:
            content= {}
        return content  
    
    
    def get_image(link):
        url = link
        session = HTMLSession()
        req= session.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36 Edg/99.0.1150.46'})
        soup = BeautifulSoup(req.content, 'html.parser')
        try:
            meta_image = soup.find('meta', property="og:image").attrs['content']
        except:
            meta_image = ""
        return meta_image

