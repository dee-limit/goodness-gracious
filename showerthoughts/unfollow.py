import time
import random

import pymysql
import twitter

import db_login
import tw_auth

def unfollow():
    """
    Unfollows users who have not followed back after 1 day
    """
    check_unfollow = []
    my_followers = []
    to_unfollow = []

    connection = pymysql.connect(host=db_login.host,
                                 user=db_login.user,
                                 password=db_login.password,
                                 db=db_login.db,
                                 charset=db_login.charset)

    api = twitter.Api(consumer_key=tw_auth.details['con_key'],
                      consumer_secret=tw_auth.details['con_sec'],
                      access_token_key=tw_auth.details['acc_key'],
                      access_token_secret=tw_auth.details['acc_sec'])

    print("Unfollowing from")
    with connection.cursor() as cursor:
        cursor.execute("SELECT id FROM following WHERE date_added < DATE_SUB(NOW(), INTERVAL 1 DAY) LIMIT 0, 1000")
        for row in cursor:
            check_unfollow.append(int(row[0]))
        cursor.execute("SELECT id FROM my_followers")
        for row in cursor:
            my_followers.append(int(row[0]))

        for dude in check_unfollow:
            if dude not in my_followers:
                to_unfollow.append(dude)

        to_unfollow = to_unfollow[:10]

        for dude in to_unfollow:
            time.sleep(10)
            print("Unfollowing %d"%dude)
            try:
                unfollowed = api.DestroyFriendship(user_id=dude)
                print("Unfollowed %s"%unfollowed.screen_name)
            except Exception as e:
                print("Failed to destroy friendship for %d"%dude)
                print(str(e))
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM following WHERE id=%d"%(dude))
            connection.commit()

if __name__ == "__main__":
    unfollow()
