
import requests, re, json, sys, time
sys.stdout.reconfigure(encoding='utf-8')


#
# with open('test.html', 'r') as file:
#     text = file.read()
#     res = re.findall('\d{8}_p\d', text)
#     print('found:', len(res))
#     res = list(set(res))
#     print('trimmed:', len(res))



#
# post_key_url = 'https://accounts.pixiv.net/login?'
# login_url = 'https://accounts.pixiv.net/api/login?lang=en'
# headers = {
#     'referer': 'https://www.pixiv.net',
#     'user-agent':'PixivIOSApp/7.6.2 (iOS 12.2; iPhone9,1)'
#     # 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
# }
#
# session = requests.Session()
# pixiv_login_page = session.get(url=post_key_url,headers=headers)
# post_key = re.search(r'post_key" value="(.*?)"', pixiv_login_page.text).group(1)
# data = {
#     'pixiv_id': 'restorecyclebin@gmail.com',
#     'password': '123456',
#     'post_key': post_key
# }
# res = session.post(url=login_url, data=data, headers=headers)
# if res.status_code == 200:
#     print('success login')
# else:
#     print('failed login')
#
# params = {
#     'original_tag': "",
#     'lang': 'en',
#     'suggestion': "",
#     'tag_category': ""
# }
# time.sleep(2)
# # lang: y,
# # originalTag: o,
# # suggestion: E,
# # tagCategory: A
#
# url = 'https://app-api.pixiv.net/v1/user/illusts/'
# params = {
#             'user_id': 41689219,
#             'filter': 'for_ios',
#             'type':'illust'
#         }
# headers['App-OS'] = 'ios'
# headers['App-OS-Version'] = '12.2'
# headers['App-Version'] = '7.6.2'
# headers['User-Agent'] = 'PixivIOSApp/7.6.2 (iOS 12.2; iPhone9,1)'
# res = requests.get(url=url, headers=headers, params=params)
# print(res.text)
# print(re.findall('(\d{8})_p0', res.text))










from pikax import Pixiv
import settings

def download_search_test():
    pixiv = Pixiv()
    # results = pixiv.search(keyword='オリジナル', type='illust', dimension='horizontal', popularity=10000, limit=1)
    # pixiv.download(results)
    # results = pixiv.search(keyword='', type='illust', dimension='horizontal', popularity=5000, limit=1)
    # pixiv.download(results)
    results = pixiv.search(keyword='オリジナル', type='illust', dimension='vertical', popularity=20000, limit=1)
    pixiv.download(results)
    # results = pixiv.search(keyword='オリジナル', type='illust', dimension='square', popularity=100, limit=1)
    # pixiv.download(results)


def download_daily_rankings_test():
    pixiv = Pixiv()
    results = pixiv.rank(limit=1, content='illust', mode='daily', date=None)
    pixiv.download(results, folder='#Pixiv_daily_ranking')
    results = pixiv.rank(limit=1, content='illust', mode='monthly', date=None)
    pixiv.download(results)
    results = pixiv.rank(limit=1, content='illust', mode='weekly', date=None)
    pixiv.download(results)


if __name__ == '__main__':
    # download_search_test()
    # download_daily_rankings_test()
    p = Pixiv()
    u = p.access(pixiv_id=3872398)
    # u = p.login(settings.username, settings.password)
    print(u.id)
    print('ill:', len(u.illusts))
    print('mangas:', len(u.mangas))
    print('bookms:', len(u.bookmarks))
