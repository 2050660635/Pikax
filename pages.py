# -*- coding: utf-8 -*-

import re, time, util, settings, requests, json
from exceptions import LoginError, ReqException, PostKeyError, IDError

__all__ = ['LoginPage', 'SearchPage', 'RankingPage', 'UserPage']

# raise LoginError if failed to login
class LoginPage:
    _post_key_url = 'https://accounts.pixiv.net/login?'
    _login_url = 'https://accounts.pixiv.net/api/login?lang=en'
    headers = {
        'referer': 'https://accounts.pixiv.net/login',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
    }

    def __init__(self):
        self.session = requests.Session()

    def _get_post_key_from_pixiv(self):
        util.log('Sending request to retrieve post key ... ', end='')
        try:
            pixiv_login_page = util.req(type='get', session=self.session, url=self._post_key_url)
            res = re.search(r'post_key" value="(.*?)"', pixiv_login_page.text)
            if res:
                post_key = res.group(1)
                if post_key:
                    util.log('post key successfully retrieved:', post_key)
                    return post_key
        except ReqException as e:
            util.log(str(e), type='error save')

        raise PostKeyError('Failed to find post key')



    def login(self, username, password):
        try:
            data = {
                'pixiv_id': username,
                'password': password,
                'post_key': self._get_post_key_from_pixiv()
            }
            util.log('Sending request to attempt login ... ')
            respond = util.req(type='post', session=self.session, url=self._login_url, data=data)
            util.log('Login successfully into Pixiv as [' + str(username) + ']', type='inform')
            return self.session
        except ReqException as e:
            util.log(str(e), type='error save')
            raise LoginError('Login failed. Please check your internet or username and password in settings.py', type='inform save')


class SearchPage:
    search_url = 'https://www.pixiv.net/search.php?'
    search_popularity_postfix = u'users入り'
    search_regex = r'(\d{8})_p\d'
    popularity_list = [10000, 5000, 1000, 500] # TODO: falsey result when search with 20000

    """
    keyword: string to search
    type: manga | illust | ugoira | default any
    dimension: vertical | horizontal | square | default any
    mode: strict_tag | loose | default tag contains
    popularity: a number, add after search keyword as: number users入り, use 'popular' if you want to get better results | default date descending, all results, which is not as good usually
    limit: how many artworks to get | default all
    """

    def __init__(self):
        pass

    def get_ids(self, keyword, limit=None, type=None, dimension=None, mode=None, popularity=None):

        # if max_page is None, it will search all pages
        util.log('Start searching for id with keyword:', keyword)

        # setting parameters
        start = time.time()
        params = dict()
        if type: # default match all type
            params['type'] = type

        if dimension: # default match all ratios
            if dimension == 'horizontal':
                params['ratio'] = '0.5'
            elif dimension == 'vertical':
                params['ratio'] = '-0.5'
            elif dimension == 'square':
                params['ratio'] = '0'
            else:
                raise ValueError('Invalid dimension given:', dimension)

        if mode: # default match if contain tags
            if mode == 'strict_tag': # specified tags only
                params['s_mode'] = 's_tag_full'
            elif mode == 'loose':
                params['s_mode'] = 's_tc'
            else:
                raise ValueError('Invalid mode given:', mode)

        # search starts
        if popularity == None:
            ids = self._get_ids_helper(params=params, keyword=keyword, limit=limit, popularity=popularity)
        elif popularity == 'popular':
            for popularity in self.popularity_list:
                ids = self._get_ids_helper(params=params, keyword=keyword, limit=limit, popularity=popularity)
        else:
            ids = self._get_ids_helper(params=params, keyword=keyword, limit=limit, popularity=popularity)


        util.log('Found', str(len(ids)), 'ids for', keyword, 'in', str(time.time() - start) + 's', type='inform')
        return ids

    def _get_ids_helper(self, params, keyword, popularity, limit=None, curr_page=1, ids_sofar=[]):
        while True:
            # get a page's ids
            params['p'] = curr_page
            params['word'] = str(keyword)
            if popularity != None:
                params['word'] += ' ' + str(popularity) + self.search_popularity_postfix
            util.log('Searching id for params:', params, 'at page:', curr_page)
            try:
                err_msg = 'Failed getting ids from params ' + str(params) + ' page: ' + str(curr_page)
                results = util.req(type='get', url=self.search_url, params=params, err_msg=err_msg)
            except ReqException as e:
                util.log(str(e), type='error save')
                util.log('Failed to retrieve data from page:', curr_page, 'terminated', type='inform save')
                return ids_sofar

            ids = re.findall(self.search_regex, results.text)

            # set length of old ids and new ids,
            # use later to check if reached end of all pages
            old_len = len(ids_sofar)
            ids_sofar += ids
            ids_sofar = list(set(ids_sofar))
            new_len = len(ids_sofar)

            # if limit is specified, check if reached limited number of items
            if limit != None:
                if limit == new_len:
                    return ids_sofar
                elif limit < new_len:
                    return util.trim_to_limit(ids_sofar, limit=limit)
                # limit has not reached

            # now check if any new items is added
            if old_len == new_len: # if no new item added, end of search pages
                if limit != None: # if limit is specified, it means search ended without meeting user's limit
                    util.log('Search did not return enough items for limit:', new_len, '<', limit, type='inform save')
                return ids_sofar

            # search next page
            curr_page += 1


class RankingPage:
    url = 'https://www.pixiv.net/ranking.php?'

    def __init__(self):
        pass

    """
    mode: daily | weekly | monthly | rookie | original | male | female | default daily
    max_page: 1 page = 50 artworks | default all pages
    date: up to which date | default today, format: yyyymmdd
    content: illust | manga | ugoria | default any
    """
    def rank(self, mode='daily', limit=None, date=None, content=None):
        params = dict()
        params['format'] = 'json'
        params['mode'] = mode
        params['ref'] = 'rn-h-image-3' # fix some failures
        if date:
            params['date'] = date
        if content:
            params['content'] = content

        util.log('Start searching ranking for mode', mode, '...', type='inform')
        start = time.time()
        ids = []
        page_num = 0
        exception_count = 0
        while True:
            page_num += 1
            params['p'] = page_num
            try:
                res = util.req(type='get', url=self.url, params=params)
                res = util.json_loads(res.content)
            except (ReqException, json.JSONDecodeError) as e:
                util.log(str(e), type='error save')
                util.log('Error while loading page:', page_num , 'in ranking page', type='inform save')
                exception_count += 1
                if exception_count > settings.MAX_WHILE_TRUE_LOOP_EXCEPTIONS:
                    util.log('Too many exceptions encountered:', exceptions, 'terminating ...', type='inform save')
                    break
                else:
                    continue
            if 'error' in res:
                util.log('End of page while searching', str(params) + '. Finished')
                break
            else:
                ids += [content['illust_id'] for content in res['contents']]

            # check if number of ids reached requirement
            if limit:
                num_of_ids_found = len(ids)
                if limit == num_of_ids_found:
                    break
                elif limit < num_of_ids_found:
                    ids = util.trim_to_limit(ids, limit)
                    break

        # log results
        if limit:
            num_of_ids = len(ids)
            if limit > num_of_ids:
                util.log('Items found in ranking is less than requirement:', num_of_ids, '<', limit, type='inform')
        util.log('Done. Total ids found:', len(ids), type='inform')

        return ids

# raise IDError if failed to retrieves id, raise OtherUserPageError if failed to init
class OtherUserPage:
    data_url = 'https://www.pixiv.net/ajax/user/{pixiv_id}/illusts/bookmarks?'
    bookmark_url = 'https://www.pixiv.net/bookmark.php?'
    artwork_url = 'https://www.pixiv.net/ajax/user/{pixiv_id}/profile/all'
    params = {
        'tag': '',
        'offset': '0',
        'limit': '1',
        'rest': 'show'
    }
    """
    self vars:
        id
        title
    """

    def _add_public_fav_ids(self):
        try:
            ids_url = self.data_url.format(pixiv_id=self.id, limit=self.total_fav)
            ids_data = util.req(type='get', session=self.session, url=ids_url, params=self.params)
            ids_data = util.json_loads(ids_data.content)
            self.public_fav_ids = [artwork['id'] for artwork in ids_data['body']['works']]
            self.public_fav_ids_length = len(self.public_fav_ids)
            util.log(self.username + '\'s favs found:', self.public_fav_ids_length, type='inform')
        except (ReqException, json.JSONDecodeError) as e:
            util.log(str(e), type='error save')
            util.log('Failed to retrieve public ids data from id:', self.id, type='inform save')
            raise IDError('Failed to add public fav ids')

    def _add_illust_ids(self):
        try:
            err_msg = 'Failed to get data from id: ' + str(self.id)
            res = util.req(type='get', url=self.artwork_url.format(pixiv_id=self.id), err_msg=err_msg)
            data = util.json_loads(res.content)
            if data['error']:
                util.log('Error in returned illust data, id:', self.id , type='inform save')
                raise ReqException()
            self.data = data
            self.illust_ids = [id for id in self.data['body']['illusts']]
        except (ReqException, json.JSONDecodeError) as e:
            util.log(str(e), type='error save')
            raise IDError('Failed to add illust ids')

    def _add_manga_ids(self):
        try:
            err_msg = 'Failed to get data from id: ' + str(self.id)
            res = util.req(type='get', url=self.artwork_url.format(pixiv_id=self.id), err_msg=err_msg)
            data = util.json_loads(res.content)
            if data['error']:
                util.log('Error in returned manga data, id:', self.id , type='inform save')
                raise ReqException()
            self.data = data
            self.manga_ids = [id for id in self.data['body']['manga']]
        except (RequestException, json.JSONDecodeError) as e:
            util.log(str(e), type='error save')
            raise IDError('Failed to add manga ids')

    def __init__(self, pixiv_id, session):
        self.public_fav_ids = []
        self.id = pixiv_id
        self.session = session
        self.public_fav_ids = None
        self.illust_ids = None
        self.data = None
        self.manga_ids = None
        req_url = self.data_url.format(pixiv_id=self.id)
        err_msg = 'Error while generating user page, id: ' + str(self.id)
        try:
            res = util.req(type='get', session=self.session, url=req_url, params=self.params, err_msg=err_msg)
            data = util.json_loads(res.text)
            if data['error']:
                util.log('Error in returned manga data, id:', self.id , type='inform save')
                raise ReqException()
            self.total_fav = data['body']['total']
            title = data['body']['extraData']['meta']['title']
            self.params['limit'] = self.total_fav
            username = re.search(r'「(.*?)」', title)
            self.username = username.group(1) if username else title
        except (ReqException, json.JSONDecodeError) as e:
            util.log(str(e), type='error save')
            util.log('Failed to load data from userpage in init, id:', self.id, type='inform save')
            raise OtherUserPageError('Failed to init user page')

    def get_public_fav_ids(self, limit=None):
        self._add_public_fav_ids()
        return util.trim_to_limit(items=self.public_fav_ids, limit=limit)

    def get_illust_ids(self, limit=None):
        self._add_illust_ids()
        return util.trim_to_limit(items=self.illust_ids, limit=limit)

    def get_manga_ids(self, limit=None):
        self._add_manga_ids()
        return util.trim_to_limit(items=self.manga_ids, limit=limit)
