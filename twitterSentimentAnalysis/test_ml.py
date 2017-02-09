#import regex
import re
import csv
import nltk
import os
import global_var
#from twitterSentimentAnalysis.global_var import get_tweets
#tweets = get_tweets()

#processed_tweets = []
#start process_tweet
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

# Get tweet words


#def get_sentiment_value(my_arr):

featureList = []
stopWords = []

stopWords = getStopWordList('stopWords.txt')

inpTweets = csv.reader(open('sampleTweets.csv', 'rb'), delimiter=',', quotechar='|')
i=0
tweets = []
for row in inpTweets: 
    try:
        sentiment = row[0]
        tweet = row[1]
        processedTweet = processTweet(tweet)
        featureVector = getFeatureVector(processedTweet)
        featureList.extend(featureVector)
        tweets.append((featureVector, sentiment));
        i = i+1
    except Exception as(e):
        print str(e)    

print i        
       
featureList = list(set(featureList))
print "\n\n\n\n"
    
    # Extract feature vector for all tweets in one shote
training_set = nltk.classify.util.apply_features(extract_features, tweets)


NBClassifier = nltk.NaiveBayesClassifier.train(training_set)

    # Test the classifier
count = 0
total = 0


    # Test the classifier
testTweet = 'Congrats @ravikiranj, i heard you wrote a new tech post on sentiment analysis'
processedTestTweet = processTweet(testTweet)
print NBClassifier.classify(extract_features(getFeatureVector(processedTestTweet)))
print testTweet

for testTweet in global_var.my_arr:
    try:
        processedTestTweet = processTweet(testTweet)
        sentiment =  NBClassifier.classify(extract_features(getFeatureVector(processedTestTweet)))
        if str(sentiment) == "positive":
            count = count+1
        elif str(sentiment) == "neutral":
            count = count + 0.5
        total = total + 1;
    except Exception as(e):
        print str(e)




global_var.result = (count*1.00)/total
print global_var.result
#Output
'''
    for testTweet in my_arr:
        try:
            processedTestTweet = processTweet(testTweet)
            sentiment =  NBClassifier.classify(extract_features(getFeatureVector(processedTestTweet)))
            print sentiment
            total = total+1
            if str(sentiment) == "positive":
                count = count+1
        except Exception as(e):
                print str(e)

    print total
    print "end"
    return (count*1.00)/total
#Output
'''