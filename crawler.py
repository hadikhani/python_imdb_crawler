import os
from abc import ABC, abstractmethod
import queue
import threading
from copy import deepcopy
import json
from os import path

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

    @staticmethod
    def check_archive_path_exist():
        if path.exists('archives'):
            if path.isfile('archives'):
                os.remove('archives')
                os.mkdir('archives')
        else:
            os.mkdir('archives')

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def store(self):
        pass


class LinksListCrawler(CrawlerBase):
    def __init__(self):
        self.page_url = None
        self.items_link = dict()

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
            # self.items_link =
            for i, link in enumerate(td_tags):
                self.items_link[str(i + 1)] = {
                    'id': str(i + 1),
                    'url': get_url(link.findChild('a')['href'])
                }
            print(f'Total items: {len(self.items_link)}')

    def print_links(self):
        if self.items_link is None:
            print('Links are not crawled yet, First you should call start method')
        else:
            print('ID'.ljust(9, ' '), '|\t', 'URL')
            print('-' * 60)
            for i, link in enumerate(self.items_link.keys()):
                print(link.ljust(9, ' '), '|\t', self.items_link[link]['url'])
                print('-' * 60)

    def store(self):
        self.check_archive_path_exist()
        with open('archives/links.json', 'w') as f:
            f.write(json.dumps(self.items_link))
        print('Links saved')


class DetailsCrawler(CrawlerBase):
    def __init__(self, links_list_crawler, threads_count=1):
        self.links_list_crawler = links_list_crawler
        self.threads_count = threads_count
        self.q = queue.Queue()
        self.details = deepcopy(links_list_crawler.items_link)

    def start(self):
        print(f'Extracting Details started with {self.threads_count} threads, Please wait...')
        for item in self.details.keys():
            self.q.put(self.details[item])

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
            item = self.q.get()
            response = self.get_page_html_doc(item['url'])
            self.parser(response.text, item)
            # print(f'{url} \t qsize: {self.q.qsize()}')
            self.q.task_done()

            if self.q.empty():
                break

    def parser(self, html_doc, item):
        soup = BeautifulSoup(html_doc, 'html.parser')
        name = soup.find(
            'h1',
            attrs={'data-testid': 'hero-title-block__title'},
        )

        year = soup.find(
            'span',
            attrs={
                'class': 'sc-52284603-2 iTRONr', },
        )

        description = soup.find(
            'span',
            attrs={'data-testid': 'plot-xl'},
        )

        details = {
            'id': item['id'],
            'url': item['url'],
            'name': name.text,
            # 'name': 'name',
            'year': year.text,
            # 'year': 'year',
            'description': description.text,
            # 'description': 'description',
        }

        self.details[item['id']] = details

    def print_links(self):
        self.links_list_crawler.print_links()

    def print_details(self):
        if self.details is None:
            print('Items are not crawled yet, First you should call start method')
        else:
            for detail in self.details:
                print(
                    self.details[detail]['id'].ljust(9, ' '),
                    f"{self.details[detail]['name'].ljust(60, ' ')} \t {self.details[detail]['year']} \t {self.details[detail]['description'][:40]}"
                )

    def store(self):
        self.check_archive_path_exist()
        with open('archives/details.json', 'w') as f:
            f.write(json.dumps(self.details))
        print('Details saved')
