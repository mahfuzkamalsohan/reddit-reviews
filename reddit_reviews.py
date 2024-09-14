import praw
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from textblob import TextBlob
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from praw.models import MoreComments
import sys
import config

def main():
    reddit = praw.Reddit(user_agent=True, client_id=config.client_id, client_secret=config.client_secret)

    subreddit_name = input("SEARCH: ")
    try:
        post_count = int(input("NUMBER OF POSTS: "))
    except ValueError:
        sys.exit("Please provide an integer")
    else:
        if post_count > 300:
            sys.exit("Too many posts requested")


    driver = keep_browser_open()
    driver.get("https://www.reddit.com/search/?q="+subreddit_name)


    print("\nSearching...\n")


    infinite_scroll(driver) #scrolling to load posts

    submissions_urls_list = get_urls(driver, post_count)
    if submissions_urls_list == None or len(submissions_urls_list) == 0:
        sys.exit(f"Couldn’t find any results for '{subreddit_name}'")


    print("Posts collected:", len(submissions_urls_list))


    print("\nCollecting comments...\n")



    list_of_comments = get_comments(submissions_urls_list, reddit)
    list_of_sentiments = []
    for each_comment in list_of_comments:
        list_of_sentiments.append(comments_sentiment(each_comment))
    

    print("Comments collected: ", len(list_of_comments))


    
    df = pd.DataFrame({'comments': list_of_comments, 'sentiments': list_of_sentiments}) #creating a pandas dataframe


    print(df)


    print("\nGenerating graph...\n")
    

    df.to_csv('comments.csv', index=False)#exporting the dataframe as csv // setting index to false removes the row count index

    plot_figure(df) #generating the graph





























def get_comments(submissions_urls_list, reddit):
    comments_list = []
    for link in submissions_urls_list:
        post = reddit.submission(url="https://www.reddit.com"+link)
        post.comments.replace_more(limit=None)  # handle MoreComments object issue
        for comment in post.comments.list():
            comments_list.append(comment.body)
    return comments_list




def comments_sentiment(each_comment):
    analysis = TextBlob(each_comment)
    if analysis.sentiment.polarity > 0:
        return 'Positive'
    elif analysis.sentiment.polarity < 0:
        return 'Negative'
    else:
        return 'Neutral'
    


def keep_browser_open():
    """Enabling the 'detach' experimental option
        to keep the browser open"""
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging']) #removing DevTools error message for chromedriver issue
    options.add_experimental_option("detach", True)
    
    driver = webdriver.Chrome(options=options)
    return driver
    

def get_urls(driver, post_count):
    list_of_urls = []
    list_of_post_urls = []
    links = driver.find_elements(By.TAG_NAME, "a")
 
    for link in links:
        list_of_urls.append(link.get_attribute("href"))
       
    for urls in list_of_urls:
        if "/comments/" in urls:
            list_of_post_urls.append(urls)
        if len(list_of_post_urls) == post_count:
            return list_of_post_urls
    if len(list_of_post_urls) < post_count:
        return list_of_post_urls

        



def infinite_scroll(driver):
    """Scrolls to the bottom of a page
    and compares new page height with previous one"""

    last_height_of_page = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(2)
        new_height_of_page = driver.execute_script("return document.body.scrollHeight")
        if new_height_of_page == last_height_of_page:
            break
        else:
            last_height_of_page = new_height_of_page
            

def plot_figure(df):

    plt.figure(figsize=(10, 6))
    sns.countplot(x='sentiments', data= df, legend=False ,hue='sentiments', palette='Set2')
    plt.title('Sentiment Analysis of Comments')
    plt.xlabel('Sentiment')
    plt.ylabel('Number of Comments')
    return plt.show()


if __name__ == "__main__":
    main()