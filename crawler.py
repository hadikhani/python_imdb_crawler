from abc import ABC, abstractmethod
import threading, queue
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

        except Exception as ex:
            # print(ex)
            print('\n* Invalid input, Please try again')
            return self.get_user_choice()

    def get_page_html_doc(self, url):
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
        self.page_url = get_url(self.get_user_choice())
        response = self.get_page_html_doc(self.page_url)
        if response is None:
            print('Please check your internet connection')
        else:
            soup = BeautifulSoup(response.text, 'html.parser')
            td_tags = soup.find_all('td', attrs={'class': 'titleColumn'})
            self.list_items_link = [get_url(link.findChild('a')['href']) for link in td_tags]
            # print(f'{self.page_url}\tTotal: {len(self.list_items_link)}')

    def print_links(self):
        if self.list_items_link is None:
            print('Links are not crawled yet, First you should call start method')
        else:
            for i, link in enumerate(self.list_items_link):
                print(str(i).ljust(9, ' '), link)

    def store(self):
        NotImplemented()
