import os
import urllib.request

from bs4 import BeautifulSoup
import praw
import pymysql
import requests

import db_login

def scrape():
    """Scrapes hot posts from politicalhumor on reddit"""

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

    reddit = praw.Reddit('bot1', user_agent="scrapes politicalhumor posts by /u/BellsOfFury")
    popular_submissions = reddit.subreddit("politicalhumor").hot(limit=60)

    for submission in popular_submissions:
        if not hasattr(submission, 'post_hint'):
            submission.post_hint = 'link'
        handled = False
        if submission.post_hint == "link" or "hosted" in submission.post_hint:
            media_type = "link"
        else:
            media_type = "file"
        og_url = submission.url
        if submission.id not in scraped:
            reddit_link = "https://www.reddit.com" + submission.permalink
            if "reddit.com/r/" not in submission.url and "hosted" not in submission.post_hint and not submission.stickied:
                #imgur urls that dont link directly to image
                if submission.post_hint == "link" and "imgur" in submission.url and "gifv" not in submission.url:
                    imgur_html_doc = requests.get(submission.url)
                    soup = BeautifulSoup(imgur_html_doc.text, 'html.parser')
                    try:
                        first_url = soup.find_all('img')[0].get("src")[2:] #strip opening slashes
                        submission.url = "https://" + first_url
                        media_type = "file"
                        handled = True
                    except IndexError:
                        pass

                #img gifv urls
                if submission.post_hint == "link" and "gifv" in submission.url and not handled:
                    try:
                        imgur_html_doc = requests.get(submission.url)
                        soup = BeautifulSoup(imgur_html_doc.text, 'html.parser')
                        first_url = soup.find_all("source")[-1].get("src")[2:] #strip opening slashes
                        submission.url = "https://" + first_url
                        media_type = "file"
                        handled = True
                    except:
                        pass

                #gfycat urls
                if "gfycat" in submission.url and not handled:
                    try:
                        gyfcat_html_doc = requests.get(submission.url)
                        soup = BeautifulSoup(gyfcat_html_doc.text, 'html.parser')
                        url_list = soup.find_all("source")
                        for item in url_list:
                            if "mp4" in item.get("src"):
                                submission.url = item.get("src")
                        media_type = "file"
                        handled = True
                    except:
                        pass

                file_name = submission.id + '.' + submission.url.split('/')[-1].split('.')[-1]
                if len(file_name.split('.')[-1]) > 4:
                    media_type = "link"

            if "reddit.com/r" in submission.url:
                media_type = "link"

            if media_type == "link":
                location = og_url

            else:
                location = "/home/dima/twitter_bots/politicalhumor/media/" + file_name
                print(submission.id, submission.title, submission.url)
                try:
                    response = urllib.request.urlopen(submission.url, data=None, timeout=10)
                    response_data = response.read()
                    with open(location, 'wb') as temp_file:
                        temp_file.write(response_data)
                    print("wrote to file '%s'"%location)
                    if "jpg" in location or "jpeg" in location or "png" in location:
                        if os.path.getsize(location) > 5200000:
                            os.remove(location)
                            location = og_url
                            media_type = "link"
                    if "gif" in location:
                        if os.path.getsize(location) > 5200000:
                            os.remove(location)
                            location = og_url
                            media_type = "link"
                except urllib.error.HTTPError:
                    location = og_url
                    media_type = "link"


            with connection.cursor() as cursor:
                sql_1 = "INSERT IGNORE INTO names(id) VALUES('%s')"%submission.id
                cursor.execute(sql_1)
                sql_2 = "INSERT IGNORE INTO current(id, score, title, location, media_type)"
                sql_3 = " VALUES(%s, %s, %s, %s, %s)"
                final_sql = sql_2 + sql_3
                cursor.execute(final_sql, (submission.id, submission.score, submission.title, location, media_type))

            connection.commit()
    connection.close()

if __name__ == "__main__":
    scrape()