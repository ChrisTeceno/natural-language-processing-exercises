import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import os

git st
def get_first_page_post_links():
    response = requests.get(
        "https://codeup.com/blog/", headers={"user-agent": "Codeup DS"}
    )
    soup = BeautifulSoup(response.text)
    links = []
    for link in soup.select(".more-link"):
        if link.get("href") and link.get("href")[0:4] == "http":
            links.append(link.get("href"))
    return links


def parse_post_links(links):
    posts = []
    for link in links:
        response = requests.get(link, headers={"user-agent": "Codeup DS"})
        soup = BeautifulSoup(response.text)
        title = soup.select_one(".entry-title").text
        date = soup.select_one(".published").text
        body = soup.select_one(".entry-content").text.strip()
        posts.append({"title": title, "date": date, "body": body})
    return pd.DataFrame(posts)


def get_all_post_links():
    url = "https://codeup.com/blog/page/{}/?et_blog"
    response = requests.get(url, headers={"user-agent": "Codeup DS"})
    soup = BeautifulSoup(response.text)
    links = []
    for link in soup.select(".more-link"):
        if link.get("href") and link.get("href")[0:4] == "http":
            links.append(link.get("href"))
    return links


def get_all_posts(use_cache=True):
    """ pull all posts from codeup.com  or use the cached version """
    filename = "posts.csv"
    if use_cache and os.path.exists(filename):
        print("Using cached version of posts")
        return pd.read_csv(filename)
    print("Fetching posts from codeup.com")
    page = 1
    df = pd.DataFrame()
    url = f"https://codeup.com/blog/page/{page}/?et_blog"
    response = requests.get(url, headers={"user-agent": "Codeup DS"})
    print("woring on page 1...", end="")
    while True:  # loop until no new links are found
        print(f"\rworking on page {page}...", end="", flush=True)
        url = f"https://codeup.com/blog/page/{page}/?et_blog"
        response = requests.get(url, headers={"user-agent": "Codeup DS"})
        soup = BeautifulSoup(response.text)
        links = []
        for link in soup.select(".more-link"):
            if link.attrs["href"] and link.get("href")[0:4] == "http":
                links.append(link.get("href"))
        # print(f'links length: {len(links)}')
        if len(links) == 0:  # break when no new links are found
            break
        posts = parse_post_links(links)
        df = df.append(posts)
        page += 1
    df.reset_index(inplace=True, drop=True)
    df.to_csv(filename, index=False)
    return df


def parse_news_card(card):
    "Given a news card object, returns a dictionary of the relevant information."
    card_title = card.select_one(".news-card-title")
    output = {}
    output["title"] = card.find("span", itemprop="headline").text
    output["author"] = card.find("span", class_="author").text
    output["content"] = card.find("div", itemprop="articleBody").text
    output["date"] = card.find("span", clas="date").text
    return output


def parse_inshorts_page(url):
    """Given a url, returns a dataframe where each row is a news article from the url.
    Infers the category from the last section of the url."""
    category = url.split("/")[-1]
    response = requests.get(url, headers={"user-agent": "Codeup DS"})
    soup = BeautifulSoup(response.text)
    cards = soup.select(".news-card")
    df = pd.DataFrame([parse_news_card(card) for card in cards])
    df["category"] = category
    return df


def get_inshorts_articles(use_cache=True):
    """
    Returns a dataframe of news articles from the business, sports, technology, and entertainment sections of
    inshorts.
    """
    filename = "inshorts_articles.csv"
    if use_cache and os.path.exists(filename):
        print("Using cached version of inshorts articles")
        return pd.read_csv(filename)
    print("Fetching inshorts articles")
    url = "https://inshorts.com/en/read/"
    categories = ["business", "sports", "technology", "entertainment"]
    df = pd.DataFrame()
    for cat in categories:
        df = pd.concat([df, pd.DataFrame(parse_inshorts_page(url + cat))])
    df = df.reset_index(drop=True)
    df.to_csv(filename, index=False)
    return df
