import twitter
import pymysql

import db_login
import tw_auth

def post():
    """
    Posts to twitter and clears posted details from showerthoughts.current.
    Returns tweeted object.
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
        cursor.execute("SELECT * FROM current ORDER BY score DESC LIMIT 0, 1")
        for (post_id, score, title) in cursor:
            if int(score) > 1000 and len(title) < 240:
                tweet = api.PostUpdate(status=title,
                                       latitude="40.771032",
                                       longitude="-73.968041",
                                       verify_status_length=False)

            cursor.execute("DELETE FROM current WHERE id='%s"%post_id)
    connection.commit()
    connection.close()
    return tweet

if __name__ == "__main__":
    post()
