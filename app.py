import requests
from bs4 import BeautifulSoup
import feedcrawler


FeedPediaURL = "https://www.feedipedia.org/"
FeedPediaFeedUrl = FeedPediaURL + "/content/feeds?category=All"

# list of all URL text and href
def get_feed_items(soup):

    feed_elements = []

    html_feed_elements = soup.select('.views-view-grid.cols-2 tr a')
    for html_feed_element in html_feed_elements:
        feed_item_dic = {}
        feed_item_dic['text'] = html_feed_element.text
        feed_item_dic['href'] = FeedPediaURL + html_feed_element.get('href')
        feed_elements.append(feed_item_dic)

    return feed_elements

# get all feed link and run all functions
def enrich_feed_item(feed_item_dic):
    enriched_feed_item = {}
    feed_element_html = requests.get(feed_item_dic['href'])
    soap = BeautifulSoup(feed_element_html.text, 'html.parser')

    enriched_feed_item['name'] = feed_item_dic['text']
    enriched_feed_item['href'] = feed_item_dic['href']
    enriched_feed_item['common_names'] = feedcrawler.get_common_names(soap)
    enriched_feed_item['synonyms'] = feedcrawler.get_synonyms(soap)
    enriched_feed_item['related_feeds'] = feedcrawler.get_related_feeds(soap)
    enriched_feed_item['description'] = feedcrawler.get_description(soap)
    enriched_feed_item['extra_data'] = feedcrawler.get_extra_data(soap)
    enriched_feed_item['chemicals'] = feedcrawler.get_tables(soap)

    return enriched_feed_item
