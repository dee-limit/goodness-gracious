import praw
import pymysql
import db_login

def scrape():
    """
    Scrapes most popular posts from subreddit 'r/showerthoughts' to local db.
    """

    scraped = []
    connection = pymysql.connect(host=db_login.host,
                                 user=db_login.user,
                                 password=db_login.password,
                                 db=db_login.db,
                                 charset=db_login.charset)

    with connection.cursor() as cursor: #build list of scraped submissions
        cursor.execute("SELECT * FROM names")
        result = cursor.fetchall()
    for entry in result:
        scraped.append(entry[0])

    reddit = praw.Reddit('bot1', user_agent="scrapes showerthoughts posts by /u/BellsOfFury")
    showerthoughts = reddit.subreddit("showerthoughts").hot(limit=20)

    for submission in showerthoughts:
        if not submission.stickied:
            post_id = submission.id
            title = submission.title
            score = submission.score
            
            with connection.cursor() as cursor:
                sql_1 = "INSERT IGNORE INTO names(id) VALUES('%s')"%post_id
                cursor.execute(sql_1)
                sql_2 = "INSERT IGNORE INTO current(id, title, score)"
                sql_3 = " VALUES(%s, %s, %s)"
                final_sql = sql_2 + sql_3
                cursor.execute(final_sql, (post_id, title, score))
        connection.commit()
    connection.close()


if __name__ == "__main__":
    scrape()