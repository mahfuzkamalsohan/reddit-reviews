# REDDIT REVIEWS
input             |  analyzed comments
:-------------------------:|:-------------------------:
![](/images/reddit_reviews_demo1.png)  |  ![](/images/reddit_reviews_demo2.png)

![](/images/reddit_reviews_demo3.png)
## Description:
Analyze sentiment from Reddit comments to get an overall review of a specific search term.


## Files
- "test_reddit_reviews.py" includes tests for three of the functions from the project.

- "comments.csv" contains all the comments extracted along with the sentiment of each comment in a database format.

## Functionalities and Design Choices
- Searches through reddit with the filters "Relevance" and "All time" for posts under the provided search term.
- The number of posts a user is able to request has been limited to 300 in order to avoid overloading.
- The "infinite_scroll()" function is used to scroll to the bottom of the search page for loading maximum number of posts available.
- The "get_urls()" function firstly collects all the available links under the tag "a" and then filters out the necessary ones that contain "/comments/".
- Using the [TextBlob](https://textblob.readthedocs.io/en/dev/) library, the comments are analyzed and categorized into 3 outcomes: "Positive", "Neutral" and "Negative".
- The data is visualized using the libraries [matplotlib](https://matplotlib.org) and [seaborn](https://seaborn.pydata.org).

## Get Started
Get your own Reddit application ID and secret from Reddit. More on that [here](https://github.com/reddit-archive/reddit/wiki/OAuth2). Then, plug in the tokens at the top of reddit_reviews.py.

1. Clone this repository and install dependencies:
```sh
pip install -r requirements.txt
```
2. Run reddit_reviews.py:
```sh
python reddit_reviews.py
```

