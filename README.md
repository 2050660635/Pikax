# Pikax:unicorn:
![GitHub stars](https://img.shields.io/github/stars/Redcxx/pikax?color=000&style=flat-square) ![PyPI](https://img.shields.io/pypi/v/pikax?color=000&style=flat-square) ![PyPI - License](https://img.shields.io/pypi/l/pikax?color=000&style=flat-square) ![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/Redcxx/pikax?color=000&style=flat-square) ![GitHub last commit](https://img.shields.io/github/last-commit/Redcxx/pikax?color=000&style=flat-square) ![PyPI - Downloads](https://img.shields.io/pypi/dm/pikax?color=000&style=flat-square) <br>
Pikax的目的是提供一个使用简单且强大的[Pixiv](https://www.pixiv.net/)\[P站\]批量下载工具。
#### [English ver](https://github.com/Redcxx/Pixiv-Crawler/blob/master/README.en.md)
## 图形界面版
> 不提供翻墙，请使用VPN或者飞机
- [日志](https://github.com/Redcxx/Pikax/blob/master/gui/change_log.txt)
- 用P站账号或游客登录即可
- 支持多核下载
  - 排行榜
  - 搜索
  - 特定用户所有的插画、收藏、漫画
  - 任意URL的插画、漫画
- [下载](https://github.com/Redcxx/Pikax/blob/master/gui/dist)
## 接口版
````
  # 当前的v2跟v1不兼容，v1用户谨慎更新，deprecated文件夹有v1的源码
  pip install Pikax # 当前的发布
````
---
## 需要
- [Python3](https://www.python.org/downloads/)
- [Requests](https://2.python-requests.org/en/master/)
- 可以访问[Pixiv](https://www.pixiv.net/)的网络
```
  pip install requests
```
## 目前支持的下载功能
- 搜索
  - 关键字/标签，数量，类别，模式，受欢迎程度
- 排行榜
  - 日期，数量，模式，内容种类
- 你的或者别人的
  - 插画，漫画，收藏

## 在计划中的功能
- 搜索画师
- 作品/画师 过滤
- 。。。
- 有人再做吧，我自己够用了owo
## 试用 [demo.py](https://github.com/Redcxx/Pixiv-Crawler/blob/master/demo.py)
### [命令行展示](https://github.com/Redcxx/Pikax/blob/master/demo.gif)
### 下载当日排行榜前50的插画
````
  from pikax.pikax import Pikax

  pixiv = Pikax()
  results = pixiv.rank(limit=50)
  pixiv.download(results)
````
### 搜索并下载arknights相关，赞数约1000的50张插画
````
  from pikax.pikax import Pikax, settings, params

  pixiv = Pikax(settings.username, settings.password)
  results = pixiv.search(keyword='arknights', limit=50, popularity=1000, match=params.Match.PARTIAL)
  pixiv.download(results)
````
### 下载用户的作品 （需要登录，[settings.py](https://github.com/Redcxx/Pixiv-Crawler/blob/master/pikax/settings.py)有临时的账号）
````
  from pikax.pikax import Pikax, settings, params

  # 自己的
  pixiv = Pikax()
  user = pixiv.login(username=settings.username, password=settings.password)  # 登录
  bookmarks = user.bookmarks(limit=20)  # 获取收藏
  pixiv.download(bookmarks)  # 下载

  # 任何用户
  pixiv = Pikax()
  pixiv = Pikax(settings.username, settings.password)
  other_user = pixiv.visits(user_id=201323)  # 输入id得到用户

  illusts = other_user.illusts(limit=25)  # 获取他的画作
  pixiv.download(illusts)  # 下载

  mangas = other_user.mangas(limit=10)  # 获取他的漫画
  pixiv.download(mangas)  # 下载

  bookmarks = other_user.bookmarks(limit=20)  # 获取他的收藏
  pixiv.download(bookmarks)  # 下载
````

### 用作品id下载
````
  from pikax.pikax import Pikax

  pixiv = Pikax()
  pixiv.download(illust_id=75608670)
````
### 更多例子请参考[demo.py](https://github.com/Redcxx/Pixiv-Crawler/blob/master/demo.py)
### 更详细的接口详情请参考[models.py](https://github.com/Redcxx/Pikax/blob/master/pikax/models.py)

## 更多操作
### 下载排行榜前50且收藏高于1000的作品
````
  from pikax.pikax import Pikax

  pixiv = Pikax()
  results = pixiv.rank(limit=50)  # 排行榜前50

  new_results = results.bookmarks > 1000  # 去除收藏小于 1000
  pixiv.download(new_results)  # 下载
````

### 搜索'初音'相关的200个收藏约1000的作品并筛选出其中赞大于1000且浏览量大于20000的作品
````
  from pikax.pikax import Pikax, settings

  pixiv = Pikax(settings.username, settings.password)
  results = pixiv.search(keyword='初音', limit=200, popularity=1000)  # 搜索

  new_results = (results.bookmarks > 1000).views > 20000  # 获取 赞 > 1000 和 浏览 > 20000 的作品
  pixiv.download(new_results)  # 下载
````
### 更多操作请参考[models.py](https://github.com/Redcxx/Pikax/blob/master/pikax/models.py)
### 个性化设置请前往[settings.py](https://github.com/Redcxx/Pixiv-Crawler/blob/master/pikax/settings.py)
---
## 致v1用户
 - 我移除了一部分功能比如自动设置r18和尺寸搜索设置，这是因为为了解决登录问题我模拟了他们在安卓应用上的登录，但是手机应用有些设定是不支持的，比如我刚刚说的那两个，为了有一个统一的接口我决定移除他们。虽然我已经找到了解决的办法但是这个办法需要我大量的精力和时间去实现并且要求额外的依赖，而我只是一个可怜的学生因此只可能在以后有空的时候做一下，不过不能保证真的会做。。。
 - 现在基本上所有输入的参数都可以在params.py的找到，里面几乎涵盖了所有参数的枚举
 - 更棒的打印，现在跳过的画作只会在下载后显示，而且加入了剩余时间的估算

 ## 联系我可发邮件到[这里](mailto:weilue.luo@student.manchester.ac.uk)
