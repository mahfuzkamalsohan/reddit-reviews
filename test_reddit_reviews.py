import pytest
from reddit_reviews.reddit_reviews import comments_sentiment, get_urls, keep_browser_open, get_comments
import praw
 


def test_comments_sentiment():
    assert comments_sentiment("Its so good!") == "Positive"

def test_get_urls():
    driver = keep_browser_open()
    driver.get("https://www.reddit.com/search/?q=birds")
    post_count = 2
    assert len(get_urls(driver, post_count)) == post_count

def test_get_comments():
    reddit = praw.Reddit(user_agent=True, client_id="3xQAuutLg40SXsA8YPfd4w", client_secret="45FE95n5tXnHqgUTwITepIxRAAw1uA")
    submissions_urls_list = ["https://www.reddit.com/r/Dinosaurs/comments/14dlhe6/why_do_all_birds_have_beaks/"]
    assert type(get_comments(submissions_urls_list, reddit)) is list





