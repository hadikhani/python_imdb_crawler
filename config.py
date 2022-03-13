BASE_URL = 'https://imdb.com'

URLS = {
    'Top 250 movies': '/chart/top/',
    'Most popular movies': '/chart/moviemeter/',
    'Top 250 TV shows': '/chart/toptv/',
    'Most popular TV shows': '/chart/tvmeter/',
    'Lowest rated movies': '/chart/bottom/',
}


def get_url(url_key):
    if url_key in URLS:
        return BASE_URL + URLS[url_key]

    return BASE_URL + url_key
