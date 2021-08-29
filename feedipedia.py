import requests
from bs4 import BeautifulSoup
import json
import feedcrawler
from concurrent.futures import ThreadPoolExecutor

FeedPediaURL = "https://www.feedipedia.org/"
FeedPediaFeedUrl = FeedPediaURL + "/content/feeds?category=All"
ExportFileName = "feedpedia_data.json"

full_feed_items = []


def main():

    page_feed_ipedia = requests.get(FeedPediaFeedUrl)
    soup = BeautifulSoup(page_feed_ipedia.text, 'html.parser')

    print("getting main page items")
    feed_items = get_feed_items(soup)[0:3]

    extra_attributes =feedcrawler.get_extra_attributes(soup)
    print("starting multi threaded iterations")

    # with ThreadPoolExecutor(max_workers=1) as executor:
    #     return executor.map(get_feed_item_and_append,
    #                         feed_items,
    #                         timeout = 150)

    for feed_item in feed_items:
        full_feed_items.append(enrich_feed_item(feed_item))

    print("finished multi threaded iterations")

    print("writing data to file")

    with open(ExportFileName, 'w') as f:
        json.dump(full_feed_items, f)

    print("data is exported to " + ExportFileName)

    print("done")

# def get_feed_item_and_append(feed_item_dic):
#     try:
#         full_feed_items.append(enrich_feed_item(feed_item_dic))
#         print('enrich_feed_item done')
#     except:
#         print("an expcetion occured")


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

    enriched_feed_item['common_names'] = feedcrawler.get_common_names(soap)
    enriched_feed_item['synonyms'] = feedcrawler.get_synonyms(soap)
    enriched_feed_item['related_feeds'] = feedcrawler.get_related_feeds(soap)
    enriched_feed_item['description'] = feedcrawler.get_description(soap)
    enriched_feed_item['extra_data'] = feedcrawler.get_extra_data(soap)
    enriched_feed_item['chemicals'] = feedcrawler.get_tables(soap)

    return enriched_feed_item



def test_enrich_feed_item():
    feed_item = {}
    feed_item['text'] = "Animal hair",
    feed_item['href'] = "https://www.feedipedia.org/node/217"

    enrich_feed_item(feed_item)

#test_enrich_feed_item()
main()






