import pymysql
import twitter

import db_login
import tw_auth

def get_my_followers():
    """
    Updates my followers to local database
    """

    connection = pymysql.connect(host=db_login.host,
                                 user=db_login.user,
                                 password=db_login.password,
                                 db=db_login.db,
                                 charset=db_login.charset)

    api = twitter.Api(consumer_key=tw_auth.details['con_key'],
                      consumer_secret=tw_auth.details['con_sec'],
                      access_token_key=tw_auth.details['acc_key'],
                      access_token_secret=tw_auth.details['acc_sec'])

    with connection.cursor() as cursor:
        cursor.execute("SELECT next_cursor FROM my_followers_cursor WHERE who='wetphone'")
        next_cursor = cursor.fetchall()[0][0]

    if next_cursor == 0:
        next_cursor = -1

    my_followers = api.GetFollowerIDsPaged(screen_name="wetphone", cursor=next_cursor, count=5000)

    for follower in my_followers[2]:
        with connection.cursor() as cursor:
            cursor.execute("INSERT IGNORE INTO my_followers(id) VALUES(%d)"%(follower))
        connection.commit()

    with connection.cursor() as cursor:
        cursor.execute("UPDATE my_followers_cursor SET next_cursor=%d WHERE who='theredditbot'"%(my_followers[0]))

if __name__ == "__main__":
    get_my_followers()