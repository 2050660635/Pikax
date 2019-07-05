"""
Pixiv.search:
keyword: string to search
type: manga | illust | ugoira | default any
dimension: vertical | horizontal | square | default any
mode: strict_tag | loose | default tag contains
popularity: a number, add after search keyword as: number users入り | default search all in [500, 1000, 5000, 10000, 20000]
max_page: 1 page ~ 39 artwork | default all pages


Pixiv.rank:
mode: daily | weekly | monthly | rookie | original | male | female | default daily
max_page: 1 page = 50 artworks | default all pages
date: up to which date | default today, format: yyyymmdd
content: illust | manga | ugoria | default any

Pixiv.favorites:
username: your pixiv username
password: your pixiv password
type: public | private | default both, which of your collections want to save
"""

from pixiv import Pixiv, User
import settings
def download_daily_rankings_example():
    pixiv = Pixiv()
    results = pixiv.rank(max_page=1, content='illust', mode='daily')
    pixiv.download(results, folder='#Pixiv_daily_ranking')

def download_search_example():
    pixiv = Pixiv()
    results = pixiv.search(keyword='少女', type='illust', dimension='horizontal', popularity=10000, max_page=2)
    pixiv.download(results)

def download_others_favorites_example():
    pixiv = Pixiv()
    user = pixiv.login(username=settings.username, password=settings.password)
    favorites = user.access_favs(pixiv_id=5594793, limit=25)
    pixiv.download(favorites)

def download_own_favourites_example():
    pixiv = Pixiv()
    user = pixiv.login(username=settings.username, password=settings.password)
    favorites = user.access_favs()
    pixiv.download(favorites)

def main():
    download_daily_rankings_example()
    # download_search_example()
    # download_others_favorites_example()
    # download_own_favourites_example()

if __name__ == '__main__':
    main()
