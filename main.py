import requests
from bs4 import BeautifulSoup
from config import get_url


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


if __name__ == '__main__':
    try:
        print(f"{'#' * 15} Wellcome to IMDB crawler {'#' * 15}")
        url = get_url(get_user_choice())
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        td_tags = soup.find_all('td', attrs={'class': 'titleColumn'})
        links = [link.findChild('a')['href'] for link in td_tags]
        # for i, link in enumerate(links):
        #     print(i+1, get_url(link))

        print(f'{url}\tTotal: {len(links)}')
    except Exception as ex:
        print(ex)
