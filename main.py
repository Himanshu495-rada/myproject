from flask import Flask,render_template,request,jsonify
import tweepy
from textblob import TextBlob
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

#---------------------------------------------------------------------------

consumer_key = 'kT0SHltK17WYZEqaucLWLY542'
consumer_secret = 'LJTTvJcriY6n17bTnGMLmHKFK18ZmG3kL8CKctsXvLBfZ6Tz2S'

access_token = '1030484740846104580-CtKmGNwmoCHTFfJPUZ51b2Gk4sAzjA'
access_token_secret = '2cwRg6UOPHe9qWA77J56myaqISVT9oNqhmLOHBeXH5TIh'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)


#-------------------------------------------------------------------------

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/search",methods=["POST"])
def search():
    names = ['very_positive','positive','neutral','negative','very_negative']
    colors = ['g', 'gold', 'b', 'orange', 'r'] 

    v_n = 0
    v_p = 0
    neg = 0
    pos = 0
    neu = 0
    search_tweet = request.form.get("search_query")
    
    t = []
    text = ""
    values = []
    tweets = api.search(search_tweet, tweet_mode='extended')
    for tweet in tweets:
        polarity = TextBlob(tweet.full_text).sentiment.polarity
        if polarity > 0:
            if polarity < 0.5:
                pos += 1
            else:
                v_p += 1
        elif polarity < 0:
            if polarity > -0.5:
                neg += 1
            else:
                v_n += 1
        else:
            neu += 1
        subjectivity = TextBlob(tweet.full_text).sentiment.subjectivity
        t.append([tweet.full_text,polarity,subjectivity])
        text += str(tweet.full_text)

    values.append([v_p, pos, neu, neg, v_n])
    plt.pie(values, explode=(0,0,0,0.1,0.2), labels = names, colors = colors, autopct= '%1.1f%%',shadow=True, startangle=90)
    plt.savefig("C:\\Users\\himan\\Desktop\\Twitter_Flask_app\\static\\pie_chart.png")
    wordcloud = WordCloud().generate(text)
    plt.figure() 
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.savefig("C:\\Users\\himan\\Desktop\\Twitter_Flask_app\\static\\wordcloud.png")
    return jsonify({"success":True,"tweets":t})

app.run(debug=True)
