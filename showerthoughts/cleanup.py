import time

import pymysql
import praw
import db_login

def clean():
    """
    Clears old entries from db
    """
    print("Clearing old entries from db...")
    connection = pymysql.connect(host=db_login.host,
                                 user=db_login.user,
                                 password=db_login.password,
                                 db=db_login.db,
                                 charset=db_login.charset)
    with connection.cursor() as cursor:
        cursor.execute("SELECT id FROM current WHERE date_added < DATE_SUB(NOW(), INTERVAL 1 DAY)")
        result = cursor.fetchall()
        for (file_id) in result:
            print("Clearing %s from db..."%(file_id))
            cursor.execute("DELETE FROM current where id='%s'"%(file_id))
        connection.commit()
    print("\nDone\n!")
    connection.close()

def update_scores():
    """
    Updates scores on current db
    """
    update_id = []
    connection = pymysql.connect(host=db_login.host,
                                 user=db_login.user,
                                 password=db_login.password,
                                 db=db_login.db,
                                 charset=db_login.charset)

    with connection.cursor() as cursor:
        cursor.execute("SELECT id FROM current")
        result = cursor.fetchall()
        for entry in result:
            update_id.append(entry[0])

    reddit = praw.Reddit('bot1', user_agent="script to update showerthoughts by /u/BellsOfFury")
    for post_id in update_id:
        submission = reddit.submission(id=post_id)
        post_score = int(submission.score)

        with connection.cursor as cursor:
            cursor.execute("UPDATE current SET score=%d WHERE id='%s'"%(post_score, post_id))
            print("Set score for %s to %d"%(post_id, post_score))
        connection.commit()
        time.sleep(1)
    connection.close()

def clean_names():
    """
    Removes old entries from names
    """
    connection = pymysql.connect(host=db_login.host,
                                 user=db_login.user,
                                 password=db_login.password,
                                 db=db_login.db,
                                 charset=db_login.charset)
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM names WHERE date_added < DATE_SUB(NOW(), INTERVAL 10 DAY)")
    connection.commit()

if __name__ == "__main__":
    clean()
    update_scores()
    clean_names()