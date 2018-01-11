import time
import random

import pymysql
import twitter

import db_login
import tw_auth

def follow():
    """
    Systematically follows users following similar pages
    """

    twitter_handles = ["TheWeirdWorld", "rShowerThoughts", "TheWeirdWorld", "TheWeirdWorld", "rShowerThoughts"]
    eligible_follow = []

    connection = pymysql.connect(host=db_login.host,
                                 user=db_login.user,
                                 password=db_login.password,
                                 db=db_login.db,
                                 charset=db_login.charset)

    api = twitter.Api(consumer_key=tw_auth.details['con_key'],
                      consumer_secret=tw_auth.details['con_sec'],
                      access_token_key=tw_auth.details['acc_key'],
                      access_token_secret=tw_auth.details['acc_sec'])

    current_handle = twitter_handles[random.randint(0, len(twitter_handles)-1)]
    print("Following from %s"%current_handle)
    timeline = api.GetUserTimeline(screen_name=current_handle, include_rts=False, exclude_replies=True)
    cur_tweet_id = timeline[random.randint(0, 3)].id
    retweets = api.GetRetweets(cur_tweet_id, count=100, trim_user=False)
    print("Total number of retweets:", len(retweets))
    for tweet in retweets:
        not_following = not tweet.user.following
        has_followers = tweet.user.followers_count > 40
        if not_following and has_followers:
            eligible_follow.append(tweet.user)
    eligible_follow = eligible_follow[:20]
    print("Number of eligible friends:", len(eligible_follow))

    for follower in eligible_follow:
        time.sleep(random.randint(1, 5))
        try:
            api.CreateFriendship(user_id=follower.id)
            print("Following %s"%follower.screen_name)
            with connection.cursor() as cursor:
                cursor.execute("INSERT IGNORE INTO following(id) VALUES(%d)"%(follower.id))
            connection.commit()
        except Exception as e:
            print(str(e))
    connection.close()