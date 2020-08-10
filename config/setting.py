import random
import os

# PATH = os.path.dirname(
#     os.path.dirname(__file__)
# )

PATH = '/Volumes/Extreme SSD'

#  Default parameters
username = 'mashiro980107@gmail.com'
password = 'iloveyou123'
myuser_id = '15691732'

headers_list = [  # User-Agent setting
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.2 Safari/605.1.15',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:21.0) Gecko/20100101 Firefox/21.0',
    'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0'
]

headers = {
    'User-Agent': random.choice(headers_list),
    'referer': 'https://www.pixiv.net',
    "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
    "Accept-Encoding": "gzip, deflate, br",
    # 'cookie': get_cookie(),
}



