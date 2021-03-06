from crawler import LinksListCrawler, DetailsCrawler


if __name__ == '__main__':
    links_list_crawler = LinksListCrawler()
    links_list_crawler.start()
    # links_list_crawler.print_links()
    links_list_crawler.store()

    details_crawler = DetailsCrawler(links_list_crawler=links_list_crawler, threads_count=4)
    details_crawler.start()
    details_crawler.print_details()
    details_crawler.store()
