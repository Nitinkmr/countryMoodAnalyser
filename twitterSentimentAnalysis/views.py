from django.http import HttpResponseRedirect

from django.shortcuts import render
from .forms import NameForm
from django.http import HttpResponse
from django.shortcuts import render_to_response
from twitter import *
import urllib
import json
from countries import country_list
from global_var import get_issues
from global_var import get_tweets
# Create your views here.

selected_country = ''


t = Twitter(
    auth=OAuth('2955186811-3knD17GyGB21G1obeECLiMA5NsJTNU1tkeBG94J', 
               '7Ba84Alidfz9nAZWcb33EFW2DmeCyxr9SJoXvVYyEkzDx',
               'UtvgXDJeHGZoL8naPRBVQJBTU',
               'xUO1RzRoIqQBP5pMhiscLBDyRH9cLEUtw8WtgZ9RvFI721MR8I'))


def country_dropDown(request):
    # if this is a POST request we need to process the form data
    trending_issues = get_issues()
         
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid:
        print form
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            selected_country = form.cleaned_data['countries_drop_down']    
            
            # get woeid for the country selected

            for country in country_list:
                if country['name'] == selected_country:
                    woeid = country['woeid']
                    break

            # get trending issues
            try:
                result = t.trends.place(_id = woeid,count = 10) 
            except Exception as(e):
                print str(e)

            print result
            i = 0
            for tweet in result[0]['trends']:
               trending_issues.append({'tweet':tweet['name'],'index':i})
               print tweet['name']
               i = i+1
               if i == 10:
                break

            print trending_issues    
       #    return HttpResponseRedirect('/trending_issues')
        else:
            print "error in country selection"
    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()

    
    return render(request, 'index.html', {'form': form,'trending_issues':trending_issues})

def tweets(request, value):
        #print request.GET.
        trending_issues = get_issues()
        print trending_issues
        print value
        print "yes\n\n\n\n\n"
        print len(trending_issues)

        selected_issue = " "
        for issue in trending_issues:
            if str(issue['index']) == value:
               selected_issue = issue['tweet']
               break 
        print selected_issue
        #selected_issue = trending_issues[0]
        #print str(trending_issues[0][value])       
        tweets = get_tweets()
        try:
            r =  t.search.tweets(q = str(selected_issue),lang="en")
            for result in r['statuses']:
                tweets.append(str(result['text'].encode('utf-8')))
                #print result['text']
        except Exception as(e):
                print str(e)
        
        print tweets

        return render(request, 'tweets.html', {'tweets':tweets,'issue':selected_issue,'data':0.4})


def get_country():
    return selected_country

