from django.http import HttpResponseRedirect
import csv
import os
from django.shortcuts import render
from .forms import NameForm
from django.http import HttpResponse
from django.shortcuts import render_to_response
from twitter import *
import urllib
import json
from countries import country_list
import global_var
import time
import re
import nltk

global trending_issues
trending_issues = []
stopWords = []
featureList = []

def processTweet(tweet):
    # process the tweets

    #Convert to lower case
    tweet = tweet.lower()
    #Convert www.* or https?://* to URL
    tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))','URL',tweet)
    #Convert @username to AT_USER
    tweet = re.sub('@[^\s]+','AT_USER',tweet)
    #Remove additional white spaces
    tweet = re.sub('[\s]+', ' ', tweet)
    #Replace #word with word
    tweet = re.sub(r'#([^\s]+)', r'\1', tweet)
    #trim
    tweet = tweet.strip('\'"')
    return tweet
#end


#for tweet in tweets:
 #   processed_tweets.append(processTweet(tweet))



#print tweets
def getStopWordList(stopWordListFileName):
    #read the stopwords file and build a list
    stopWords = []
    stopWords.append('AT_USER')
    stopWords.append('URL')

    fp = open(stopWordListFileName, 'r')
    line = fp.readline()
    while line:
        word = line.strip()
        stopWords.append(word)
        line = fp.readline()
    fp.close()
    return stopWords
#end



def replaceTwoOrMore(s):
    #look for 2 or more repetitions of character and replace with the character itself
    pattern = re.compile(r"(.)\1{1,}", re.DOTALL)
    return pattern.sub(r"\1\1", s)

def extract_features(tweet):
    tweet_words = set(tweet)
    features = {}
    for word in featureList:
        features['contains(%s)' % word] = (word in tweet_words)
    return features

def getFeatureVector(tweet):
    featureVector = []
    #split tweet into words
    words = tweet.split()
    for w in words:
        #replace two or more with two occurrences
        w = replaceTwoOrMore(w)
        #strip punctuation
        w = w.strip('\'"?,.')
        #check if the word stats with an alphabet
        val = re.search(r"^[a-zA-Z][a-zA-Z0-9]*$", w)
        #ignore if it is a stop word
        if(w in stopWords or val is None):
            continue
        else:
            featureVector.append(w.lower())
    return featureVector
#end

#from .pre_process_tweets import getFeatureVector,extract_features, processTweet

# Create your views here.

selected_country = ''


t = Twitter(
    auth=OAuth('2955186811-3knD17GyGB21G1obeECLiMA5NsJTNU1tkeBG94J', 
               '7Ba84Alidfz9nAZWcb33EFW2DmeCyxr9SJoXvVYyEkzDx',
               'UtvgXDJeHGZoL8naPRBVQJBTU',
               'xUO1RzRoIqQBP5pMhiscLBDyRH9cLEUtw8WtgZ9RvFI721MR8I'))


def country_dropDown(request):
    # if this is a POST request we need to process the form data
    #trending_issues = get_issues()
    
    #trending_issues = []
    #global_var.trending_issues = trending_issues
    
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid:
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

            i = 0
            for tweet in result[0]['trends']:
               trending_issues.append({'tweet':tweet['name'],'index':i})
               i = i+1
               if i == 10:
                break
           # global_var.set_issues(trending_issues)   
            #global_var.trending_issues = trending_issues
           # print global_var.trending_issues 
            print trending_issues
            print "issues \n\n\n"        
           # return HttpResponseRedirect('/trending_issues')
        else:
            print "error in country selection"
    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()      
    
    #global_var.set_issues(trending_issues)

    
    return render(request, 'index.html', {'form': form,'trending_issues':trending_issues})

def tweets(request, value):
        #print request.GET.
        #trending_issues = get_issues()
        #print trending_issues
        #print value
        #print "yes\n\n\n\n\n"
        #print len(trending_issues)


        selected_issue = ""
        print len(trending_issues)
        
        for issue in trending_issues:
            if str(issue['index']) == value:
               selected_issue = issue['tweet']
               break 

        print selected_issue
        print"issue is above"
       
        tweets = []
        try:
            r =  t.search.tweets(q = selected_issue,lang="en")
            for result in r['statuses']:
                tweets.append(str(result['text'].encode('utf-8')))
                #print result['text']
        except Exception as(e):
                print str(e)
        
        temp = tweets
        global_var.my_arr = tweets        
        import test_ml
        print global_var.result



        
        return render(request, 'tweets.html', {'tweets':tweets,'issue':selected_issue,'data':global_var.result})


def get_country():
    return selected_country

