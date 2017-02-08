from django.shortcuts import render

from django.http import HttpResponseRedirect

from .forms import NameForm

from twitter import *
import urllib
import json
from countries import country_list
# Create your views here.

selected_country = ''


t = Twitter(
    auth=OAuth('2955186811-3knD17GyGB21G1obeECLiMA5NsJTNU1tkeBG94J', 
               '7Ba84Alidfz9nAZWcb33EFW2DmeCyxr9SJoXvVYyEkzDx',
               'UtvgXDJeHGZoL8naPRBVQJBTU',
               'xUO1RzRoIqQBP5pMhiscLBDyRH9cLEUtw8WtgZ9RvFI721MR8I'))


def country_dropDown(request):
    # if this is a POST request we need to process the form data
    trending_issues = []
         
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid:
        print form
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            selected_country =  form.cleaned_data['countries_drop_down']    
            
            # get woeid for the country selected

            for country in country_list:
                if country['name'] == selected_country:
                    woeid = country['woeid']
                    break

            # get trending issues
            try:
                result = t.trends.place(_id = woeid) 
            except Exception as(e):
                print str(e)

            for tweet in result[0]['trends']:
               trending_issues.append(tweet['name'])
               print tweet['name']

            print trending_issues    
       #    return HttpResponseRedirect('/trending_issues')
        else:
            print "error in country selection"
    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()

    
    return render(request, 'index.html', {'form': form,'trending_issues':trending_issues})


def get_country():
    return selected_country