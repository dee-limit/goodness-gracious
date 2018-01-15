import os
import time

import twitter
import pymysql

import db_login
import tw_auth


def post():
    """
    Posts to twitter and deletes post details from theredditbot.current
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
        cursor.execute("SELECT id, score, title, location, media_type FROM current ORDER BY score DESC LIMIT 0, 1")
        for (post_id, score, title, location, media_type) in cursor:
            print(media_type)
            if media_type == "link":
                print(post_id, score)
                caption = title + """\n\n%s\n\n"""%(location)
                api.PostUpdate(status=caption, verify_status_length=False)
            else:
                caption = title
                if "mp4" in location or "gif" in location:
                    print("Posting video")
                    sleep_time = 0
                    while sleep_time < 300:
                        try:
                            time.sleep(sleep_time)
                            with open(location, 'rb') as temp_file:
                                media_id = api.UploadMediaChunked(temp_file)
                            api.PostUpdate(caption, media_id, verify_status_length=False)
                            sleep_time = 400
                            print(sleep_time)
                        except:
                            sleep_time = sleep_time + 30
                else:
                    api.PostUpdate(caption, media=location, verify_status_length=False)
                os.remove(location)
            cursor.execute("DELETE FROM current WHERE id='%s'"%post_id)
    connection.commit()
    connection.close()

if __name__ == "__main__":
    post()