from views import get_country   


# Put in token, token_key, con_secret, con_secret_key

selected_country = get_country()




'''
trending_tweets = []
with open('woeid.json') as data_file:
    woeid_list = json.load(data_file)

length = len(woeid_list)
print length

with open("trending_tweets.json",mode="r") as tweets_file:
    #feeds = json.load(tweets_file)
    #tweets_file.write(json.dumps([]))
    feeds = json.load(tweets_file)

    for i in range(0,length):
            try:    
                print str(woeid_list[i]['country_name'])
                r = t.trends.place(_id = woeid_list[i]['woeid']) 
                print r

                element = {};
                print len(r[0]['trends'])
                print "\n\n\n\n\n"
                for j in range(0,len(r[0]['trends'])):
                    element[str(j)] = r[0]['trends'][j]['name']
                    feeds[0][woeid_list[i]['country_name']]['tweets'][j] = element[str(j)]
                    #r[0]['trends'][j]['name']

            except Exception as e: 
                print str(e)


with open("trending_tweets.json",mode="w") as tweets_file:
    try:
         tweets_file.write(json.dumps(feeds))
    except Exception as e: 
                print str(e)
'''