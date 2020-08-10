"""
共有函数
"""
import requests
from lxml import etree
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ChromeOptions
from time import sleep
from config.setting import *

path = os.path.dirname(
    os.path.dirname(__file__)
)

# path = os.path.join(
#     path, 'tools'
# )
# sys.path.append(path)
chrome_path = os.path.join(
    path, 'tools', 'chromedriver'
)


def get_ips():  # Proxyをとる関数
    """

    :return IP LIST:
    """
    key_url = 'https://ip.ihuan.me/mouse.do'
    post_url = 'https://ip.ihuan.me/tqdl.html'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/84.0.4147.89 Safari/537.36',
        'referer': 'https://ip.ihuan.me/ti.html',
        'cookie': '__cfduid=d60f87035400792750819765506f990161595853071; '
                  'Hm_lvt_8ccd0ef22095c2eebfe4cd6187dea829=1595853075,1595853380,1595854703; '
                  'statistics=4c32a719821394961a4ade1553afbd48; Hm_lpvt_8ccd0ef22095c2eebfe4cd6187dea829=1595944140 '
    }
    data = {
        'num': '20',
        'port': '',
        'kill_port': '',
        'address': '日本',
        'kill_address': '',
        'anonymity': '',
        'type': '0',
        'post': '',
        'sort': '',
        'key': '',
    }
    page_text = requests.get(url=key_url, headers=headers).text
    re_re = '.val(.*?);'
    key = re.findall(re_re, page_text, re.S)[0].strip('(').strip(')').strip('"')
    data['key'] = key
    post = requests.post(url=post_url, headers=headers, data=data).text
    tree = etree.HTML(post)
    ips = tree.xpath('//div[2]/div/div[2]/text()')
    if len(ips) == 20:
        print('Proxy get successful...')
        proxy = []
        for ip in ips:
            ip_dict = {
                'http': ip
            }
            proxy.append(ip_dict)
        return proxy
    else:
        print('Proxy get Error...')


def get_cookie(art_id):  # seleniumを使って、cookieをGET
    global username
    global password

    chrome_options = Options()  # Headless　設定
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')

    option = ChromeOptions()  # Chromedriver の設定
    option.add_experimental_option('excludeSwitches', ['enable-automation'])
    bro = webdriver.Chrome(executable_path=chrome_path,
                           chrome_options=chrome_options, options=option)

    # bro = webdriver.Chrome(executable_path=chrome_path, chrome_options = chrome_options)
    # bro = webdriver.Chrome(executable_path=chrome_path)

    url = 'https://accounts.pixiv.net/login?return_to=https%3A%2F%2Fwww.pixiv.net%2Fen%2Fusers%2F' + art_id + '&lang=en&source=pc&view_type=page'
    bro.get(url)
    if username is None:
        username = str(input("Please enter your username\n---->"))
    if password is None:
        password = str(input("Please enter your password\n---->"))
    user_tag = bro.find_element_by_xpath(
        '//*[@id="LoginComponent"]/form/div[1]/div[1]/input')  # xpathでログインボタンを定位
    user_tag.send_keys(username)
    sleep(0.5)
    pass_tag = bro.find_element_by_xpath('//*[@id="LoginComponent"]/form/div[1]/div[2]/input')
    pass_tag.send_keys(password)
    bro.find_element_by_xpath('//*[@id="LoginComponent"]/form/button').click()
    sleep(1)
    cookie_item = bro.get_cookies()  # Cookieを獲得
    cookie_str = ''
    # page_text = bro.page_source
    # print(page_text)
    bro.quit()

    for item_cookie in cookie_item:  # dict cookie
        item_str = item_cookie["name"] + "=" + item_cookie["value"] + ";"
        cookie_str += item_str

    return cookie_str


if __name__ == '__main__':
    cookie = get_cookie('9016')
    print(cookie)
    # get_cookie('9016')
