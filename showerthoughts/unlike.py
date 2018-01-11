import time
import datetime
import random

import pymysql
import twitter

import db_login
import tw_auth

def unlike():
    """
    Unfavorites tweets that were favorited a day ago
    """
    to_unfavorite = []
    connection = pymysql.connect(host=db_login.host,
                                 user=db_login.user,
                                 password=db_login.password,
                                 db=db_login.db,
                                 charset=db_login.charset)

    api = twitter.Api(consumer_key=tw_auth.details['con_key'],
                      consumer_secret=tw_auth.details['con_sec'],
                      access_token_key=tw_auth.details['acc_key'],
                      access_token_secret=tw_auth.details['acc_sec'])
    print("Clearing likes...")

    with connection.cursor() as cursor:
        cursor.execute("SELECT status FROM favorited_tweets WHERE date_added < DATE_SUB(NOW(), INTERVAL 3 DAY) LIMIT 0, 20")
        for row in cursor:
            to_unfavorite.append(int(row[0]))
        for unfavorite_id in to_unfavorite:
            print("Unfavoriting status id: %d"%unfavorite_id)
            try:
                time.sleep(2)
                api.DestroyFavorite(status_id=unfavorite_id)
                print("Unfavorited")
            except twitter.error.TwitterError:
                print("failed to unfavorite")
            cursor.execute("DELETE FROM favorited_tweets WHERE status=%d"%(unfavorite_id))
            connection.commit()
            print("Cleared from database")
    connection.commit()
    connection.close()
    print("\nDone!")

if __name__ == "__main__":
    unlike()