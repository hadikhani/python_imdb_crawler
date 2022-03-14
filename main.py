import threading, queue
import requests
from bs4 import BeautifulSoup
from config import URLS, get_url
from crawler import LinksListCrawler

q = queue.Queue()


def get_user_choice():
    try:
        choices = [
            'Top 250 movies',
            'Most popular movies',
            'Top 250 TV shows',
            'Most popular TV shows',
            'Lowest rated movies',
            'Exit'
        ]

        for i, choice in enumerate(choices):
            print(i + 1, choice)
        user_choice = int(input('\nPlease select action(e.g., 1): ')) - 1

        if user_choice in range(0, 5):
            return choices[user_choice]
        elif user_choice == 5:
            exit()
        else:
            print('\n* Invalid input, Please try again')
            return get_user_choice()

    except Exception as ex:
        # print(ex)
        print('\n* Invalid input, Please try again')
        return get_user_choice()


def get_page(page_url):
    try:
        response = requests.get(page_url)
    except:
        return None

    return response


def get_movie_details_worker():
    while True:
        res2 = get_page(q.get())
        soup_details = BeautifulSoup(res2.text, 'html.parser')
        description = soup_details.find(
            'span',
            attrs={'class': 'GenresAndPlot__TextContainerBreakpointXL-sc-cum89p-2 eqbKRZ'},
        )
        print('*' * 20)
        print(description.text, q.qsize())
        print('*' * 20, '\n')
        q.task_done()

        if q.empty():
            break


if __name__ == '__main__':
    # try:
    #     print(f"{'#' * 15} Wellcome to IMDB crawler {'#' * 15}")
    #     url = get_url(get_user_choice())
    #     res = get_page(page_url=url)
    #     soup = BeautifulSoup(res.text, 'html.parser')
    #     td_tags = soup.find_all('td', attrs={'class': 'titleColumn'})
    #     links = [link.findChild('a')['href'] for link in td_tags]
    #     print(f'{url}\tTotal: {len(links)}')
    #
    #     for i, link in enumerate(links):
    #         # print(i+1, get_url(link))
    #         q.put(get_url(link))
    #
    #     threads = list()
    #     for i in range(4):
    #         t = threading.Thread(target=get_movie_details_worker)
    #         t.setDaemon(True)
    #         threads.append(t)
    #         t.start()
    #
    #     for tr in threads:
    #         tr.join()
    #
    #     q.join()
    #
    # except Exception as ex:
    #     print(ex)

    links_list_crawler = LinksListCrawler()
    links_list_crawler.start()
    links_list_crawler.print_links()
