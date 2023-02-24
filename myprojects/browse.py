from django.utils import timezone
from django.shortcuts import render
from urllib.request import urlopen
import json
from django.http import HttpResponse
from myprojects.models import searchData
import ast

def request_data(url):
    print('Requesting Data...')
    response = urlopen(url)
    data_json = json.loads(response.read())
    if data_json['Response']=='True':
        results = validate_results(data_json['Search'])
        if len(results)<10:
            print('2nd Page loading...')
            url += '&page=2'
            response = urlopen(url)
            data_json = json.loads(response.read())
            if data_json['Response']=='True':
                print('2nd Page sucessful...')
                more_results = validate_results(data_json['Search'])
                results += more_results
        return results
    else:
        return False

def save_search(orgQuery, results):
    print('Saving new search...')
    if not searchData.objects.filter(query=orgQuery).exists():
        ins = searchData(query=orgQuery, results=results, updatedOn=timezone.now(), added=timezone.now())
        ins.save()

def omdbapi(request, orgQuery):
    query = (orgQuery.strip()).replace(' ', "%20\\")
    url = 'https://www.omdbapi.com/?apikey=1299fe2c&r=json&s='+query
    filter_results = request_data(url)
    if not filter_results == False:
        print('Search Successful')
        save_search(orgQuery, filter_results)
        return return_results(request, filter_results)
    else:
        print('No Results found')
        return render(request, 'projects/browse.html',context={'search':False})        

def validate_results(results):
    filter_results = []
    for result in results:
        if not result['Poster'] == 'N/A':
            filter_results.append(result)
    return filter_results

def return_results(request, results):
    context = {'results':results, 'search':True}
    return render(request, 'projects/browse.html',context)

def updateData(request, orgQuery):
    query = (orgQuery.strip()).replace(' ', "%20\\")
    url = 'https://www.omdbapi.com/?apikey=1299fe2c&r=json&s='+query
    filter_results = request_data(url)
    if not filter_results==False:
        (searchData.objects.filter(query=orgQuery)).update(results=filter_results, updatedOn=timezone.now())
        return return_results(request, filter_results)
    else:
        return render(request, 'projects/browse.html',context={'search':False})        

def browse(request):
    if request.method == 'POST':
        query = (request.POST['query']).lower()
        orgQuery = query.strip()
        if not searchData.objects.filter(query=orgQuery).exists():
            print("Making API Request...")
            return omdbapi(request, query)
        else:
            print("Results from database...")
            lastupdated = searchData.objects.get(query=orgQuery).updatedOn
            if((timezone.now()-lastupdated).days>=10):
                print('Updating Data...')
                return updateData(request, orgQuery)
            s = searchData.objects.get(query=orgQuery).results
            try:
                results =ast.literal_eval(s)
            except:
                return omdbapi(request, orgQuery)
        return return_results(request, results)
    else:
        return render(request, 'projects/browse.html', context={'search':False})
