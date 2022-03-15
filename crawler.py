from abc import ABC, abstractmethod
import queue
import threading

import requests
from bs4 import BeautifulSoup

from config import URLS, get_url


class CrawlerBase(ABC):

    def get_user_choice(self):
        try:
            choices = list(URLS.keys())
            choices.append('Exit')

            for i, choice in enumerate(choices):
                print(i + 1, choice)
            user_choice = int(input('\nPlease select action(e.g., 1): ')) - 1

            if user_choice <= len(choices) - 1:
                # print(f'User choice: {user_choice} \t len: {len(choices)}')
                if choices[user_choice] == 'Exit':
                    print('Exit')
                    exit(1)
                else:
                    # print(choices[user_choice])
                    return choices[user_choice]
            else:
                print('\n* Invalid input, Please try again')
                return self.get_user_choice()

        except:
            # print(ex)
            print('\n* Invalid input, Please try again')
            return self.get_user_choice()

    @staticmethod
    def get_page_html_doc(url):
        try:
            response = requests.get(url)
        except Exception as ex:
            print(ex)
            return None

        return response

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def store(self):
        pass


class LinksListCrawler(CrawlerBase):
    def __init__(self):
        self.page_url = None
        self.list_items_link = None

    def start(self):
        print('*' * 40, 'IMDB Crawler', '*' * 40)
        self.page_url = get_url(self.get_user_choice())
        print('Extracting links, Please wait...')
        response = self.get_page_html_doc(self.page_url)
        if response is None:
            print('Please check your internet connection')
        else:
            soup = BeautifulSoup(response.text, 'html.parser')
            td_tags = soup.find_all('td', attrs={'class': 'titleColumn'})
            self.list_items_link = [get_url(link.findChild('a')['href']) for link in td_tags]
            print(f'Total items: {len(self.list_items_link)}')

    def print_links(self):
        if self.list_items_link is None:
            print('Links are not crawled yet, First you should call start method')
        else:
            for i, link in enumerate(self.list_items_link):
                print(str(i + 1).ljust(9, ' '), link)

    def store(self):
        NotImplemented()


class DetailsCrawler(CrawlerBase):
    def __init__(self, links_list_crawler, threads_count=1):
        self.links_list_crawler = links_list_crawler
        self.threads_count = threads_count
        self.q = queue.Queue()
        self.list_details = list()

    def start(self):
        print(f'Extracting Details started with {self.threads_count} threads, Please wait...')
        for link in self.links_list_crawler.list_items_link:
            self.q.put(link)

        threads = list()
        for i in range(self.threads_count + 1):
            t = threading.Thread(target=self.worker)
            t.setDaemon(True)
            threads.append(t)
            t.start()

        for tr in threads:
            tr.join()

        self.q.join()

    def worker(self):
        while True:
            url = self.q.get()
            response = self.get_page_html_doc(url)
            self.parser(response.text)
            # print(f'{url} \t qsize: {self.q.qsize()}')
            self.q.task_done()

            if self.q.empty():
                break

    def parser(self, html_doc):
        soup = BeautifulSoup(html_doc, 'html.parser')
        name = soup.find(
            'h1',
            attrs={'class': 'TitleHeader__TitleText-sc-1wu6n3d-0'},
        )

        year = soup.find(
            'a',
            attrs={'class': 'ipc-link ipc-link--baseAlt ipc-link--inherit-color TitleBlockMetaData__StyledTextLink-sc-12ein40-1 rgaOW',},
        )

        description = soup.find(
            'span',
            attrs={'class': 'GenresAndPlot__TextContainerBreakpointXL-sc-cum89p-2 eqbKRZ'},
        )

        details = {
            'name': name.text,
            'year': year.text,
            'description': description.text,
        }

        self.list_details.append(details)

    def print_links(self):
        self.links_list_crawler.print_links()

    def print_details(self):
        if self.list_details is None:
            print('Items are not crawled yet, First you should call start method')
        else:
            for i, detail in enumerate(self.list_details):
                print(
                    str(i + 1).ljust(9, ' '),
                    f"{detail['name'].ljust(60, ' ')} \t {detail['year']} \t {detail['description'][:40]}"
                )

    def store(self):
        NotImplemented()
