
#trending_issues = []
tweets = []
my_arr = []
NBClassifier = " "
result = 0
#trending_issues.update('issues':{})

def get_issues():
	return trending_issues

def set_issues(issues):
	trending_issues =  issues

def get_tweets():
    return tweets


def set_NBClassifier(classifier):
	NBClassifier = classifier
	testTweet = 'good'
	processedTestTweet = processTweet(testTweet)
	'''print "\n\n\n\n\n\n\n"

	print NBClassifier.classify(extract_features(getFeatureVector(processedTestTweet)))
	print "\n\n\n\n\n\n\n"'''

def get_NBClassifier():
	return NBClassifier



def get_arr():
	return my_arr

def set_arr(arr):
	my_arr = arr