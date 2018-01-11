import time
import datetime
import random

import pymysql
import twitter

import db_login
import tw_auth

def random_like():
    """
    Likes tweets dependant on certain key search terms
    """
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    eligible_tweets = []
    search_terms = ["#showerthought", "#showerthoughts", "showerthought"]
    dirty_words = ["fuck", "cock", "sex", "anal", "pussy", "blowjob", "porn"]

    connection = pymysql.connect(host=db_login.host,
                                 user=db_login.user,
                                 password=db_login.password,
                                 db=db_login.db,
                                 charset=db_login.charset)

    api = twitter.Api(consumer_key=tw_auth.details['con_key'],
                      consumer_secret=tw_auth.details['con_sec'],
                      access_token_key=tw_auth.details['acc_key'],
                      access_token_secret=tw_auth.details['acc_sec'])

    search_key_word = search_terms[random.randint(0, len(search_terms)-1)]
    print("Searching with keyword '%s'"%search_key_word)
    raw_tweets = api.GetSearch(term=search_key_word, since=today, count=100, result_type="recent", include_entities=True)
    print("Found %d tweets"%len(raw_tweets))
    for tweet in raw_tweets:
        clean = True
        not_favorited = not tweet.favorited
        for dirty_word in dirty_words:
            if dirty_word in tweet.text:
                clean = False
        if not_favorited and clean:
            eligible_tweets.append(tweet.id)

    eligible_tweets = eligible_tweets [:40]
    print("%d tweets eligible"%len(eligible_tweets))
    for eligible_tweet in eligible_tweets:
        time.sleep(random.randint(1, 3))
        try:
            api.CreateFavorite(status_id=eligible_tweet)
            print("liked %d"%eligible_tweet)
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO favorited_tweets(status) VALUES(%d)"%(eligible_tweet))
                connection.commit()
        except:
            print("Failed to like")
        connection.commit()
    connection.close()
    print("Done")

if __name__ == "__main__":
    random_like()
