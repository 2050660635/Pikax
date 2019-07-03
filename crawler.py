from pixiv import Pixiv




"""
Pixiv.search:
keyword: string to search
type: manga | illust | ugoira | default any
dimension: vertical | horizontal | square | default any
mode: strict_tag | loose | default tag contains
popularity: a number, add after search keyword as: number users入り | default search all in [500, 1000, 5000, 10000, 20000]
page: which page of the search results to crawl | default all pages


Pixiv.rank:
mode: daily | weekly | monthly | rookie | original | male | female | default daily
max_page: 1 page = 50 artworks | default all pages
date: up to which date | default today, format: yyyymmdd
content: illust | manga | ugoria | default any
"""


if __name__ == '__main__':
    pixiv = Pixiv()
    results = pixiv.search(keyword='少女', type='illust', dimension='horizontal', popularity=10000)
    pixiv.download(results)
    results = pixiv.rank(max_page=1, content='illust', mode='daily')
    pixiv.download(results)
