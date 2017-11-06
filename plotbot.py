import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
import pandas as pd
import tweepy
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import time
from datetime import datetime

# Twitter API Keys
consumer_key = "f7PaQ0IQ8ChJMdAwHkSbzBnzP"
consumer_secret = "qHNLfBiaPfOQ5Rqrp4nMGsWaxm6mVZOqznREWkR2q0LBcKQKNI"
access_token = "922262061664690179-Igw7ycjlG5hbh5C6uyOwo2YXsCqRmJ4"
access_token_secret = "C0s2qYHKkd46etovc9KxN8EXJDRO6g6NCFCEbUC1NjSnC"

# Twitter credentials
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, parser=tweepy.parsers.JSONParser(), wait_on_rate_limit = True, wait_on_rate_limit_notify = True)

#Sentiment Analyzer
analyzer = SentimentIntensityAnalyzer()

def plotbot():
    print("start")
    #Search for the mentions
    mentions = api.search("@sentient_ronbot", count=1, result_type="recent")
    print("found mentions")
    try:
        for tweet in mentions["statuses"]:
            validate = False
            text = tweet["text"]
            stpt = text.find("@",text.find("@")+1)+1
            user = text[stpt:]
            print(user)
            print(len(user))
            if len(user) > 1:
                print("have to check")
                #check if bot has already analyzed the user
                validate = CheckUser(user)
                print(validate)
                if validate == True:
                    print("validated")
                    thanks = tweet["user"]["screen_name"]
                    print(thanks)
                    #perform analysis
                    anlyz(user, thanks)
                    break
                else:
                    return print("already analyzed")
    except:
        return print("nothing happened")
    return print("woo") 

def anlyz(u,t):
    print("analyzing")
    i = 0
    k = 0
    df = pd.DataFrame({})
    df["tweet"] = ""
    df["polarity"] = ""
    df["tweet ago"] = ""
#     base = api.user_timeline(screen_name = u, count = 1)
#     #find max id to avoid potential overlap
#     for tweet in base:
#         print(json.dumps(tweet, sort_keys=True, indent=4, separators=(',', ': ')))
#         m_id = tweet["id_str"]
#         print(m_id)
    #retrieve tweets, analyze text, store in dataframe
    for v in range(1,6):
        timeline = api.user_timeline(screen_name = u, count = 100, page = v)#max_id = m_id
        for tweet in timeline:
            text = tweet["text"]
            print(text)
            polar = analyzer.polarity_scores(text)["compound"]
            print(polar)
            df.set_value(i, "tweet", text)
            df.set_value(i, "polarity", polar)
            df.set_value(i, "tweet ago", k)
            i = i + 1
            k = k - 1
            print(k)
    #plot results
    plt.clf()
    plt.plot(df["tweet ago"], df["polarity"], marker = "o", linewidth = .5, label = "@"+str(u))
    plt.ylim(-1.03, 1.03)
    plt.title("Sentiment Analysis of Tweets \n (" + str(datetime.now())[:str(datetime.now()).find(" ")]+")")
    plt.ylabel("Tweet Sentiment Score")
    plt.xlabel("Tweets Ago")
    plt.legend(title = "Tweets", loc = "best", bbox_to_anchor=(1.13, 1.18), fontsize = "small")
    plt.grid(True)
    plt.savefig("plot.png")
    med_id = api.media_upload("plot.png")
    status = "New tweet analysis: @" + str(u) + " (thanks @" + str(t) + "!)"
    api.update_status(status, media_ids = [med_id["media_id"]])
    print("success!")

def CheckUser(a):
    print("checking")
    record = api.user_timeline()
    for each in record:
        if a in each["text"]:
            return False
    return True

# Set timer to run every 5 minutes
while(True):
    print("plotbot go")
    plotbot()
    print("complete")
    time.sleep(300)