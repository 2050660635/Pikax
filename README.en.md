# Pixiv-Crawler

### Dependencies
- Python3
- Requests

### Currently supported features
- search
- ranking
- user favorites

### Try
##### run/edit&run [demo.py](https://github.com/Redcxx/Pixiv-Crawler/blob/master/demo.py) directly or create a new python file
##### download today's top 50 illustration
````
  """
  Pixiv.rank parameters:
  mode: daily | weekly | monthly | rookie | original | male | female | default daily
  max_page: 1 page = 50 artworks | default all pages
  date: up to which date | default today, format: yyyymmdd
  content: illust | manga | ugoria | default any
  """
  from pixiv import Pixiv
  pixiv = Pixiv()
  results = pixiv.rank(max_page=1, content='illust', mode='daily')
  pixiv.download(results, folder='#Pixiv_daily_ranking')
````
##### search and download horizontal illustration of keyword: young girl with 10000 likes (approx)
````
  """
  Pixiv.search parameters:
  keyword: string to search
  type: manga | illust | ugoira | default any
  dimension: vertical | horizontal | square | default any
  mode: strict_tag | loose | default tag contains
  popularity: a number, add after search keyword as: number users入り | default search all in [500, 1000, 5000, 10000, 20000]
  max_page: 1 page ~ 39 artwork | default all pages
  """
  from pixiv import Pixiv
  pixiv = Pixiv()
  pixiv.download(results)
  results = pixiv.search(keyword='少女', type='illust', dimension='horizontal', popularity=10000)
  pixiv.download(results, folder='#Pixiv_search')
````
##### Download artwork in favorites（Need to change username and password in settings.py if you want to download yours）
````
  """
  Pixiv.favorites:
  username: your pixiv username
  password: your pixiv password
  type: public | private | default both, which of your collections want to save
  """
  # yours
  pixiv = Pixiv()
  user = pixiv.login(username=settings.username, password=settings.password)
  favorites = user.access_favs()
  pixiv.download(favorites)

  # others
  pixiv = Pixiv()
  user = pixiv.login(username=settings.username, password=settings.password)
  favorites = user.access_favs(pixiv_id=5594793, limit=25)
  pixiv.download(favorites)
````
##### For more examples visit [demo.py](https://github.com/Redcxx/Pixiv-Crawler/blob/master/demo.py)
