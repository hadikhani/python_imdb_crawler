import threading, queue
import requests
from bs4 import BeautifulSoup
from config import URLS, get_url
from crawler import LinksListCrawler, DetailsCrawler


if __name__ == '__main__':
    links_list_crawler = LinksListCrawler()
    links_list_crawler.start()

    details_crawler = DetailsCrawler(links_list_crawler=links_list_crawler, threads_count=4)
    details_crawler.start()
    details_crawler.print_details()
