"""
共有函数
"""
import requests
from lxml import etree
import re
from config.setting import *

path = os.path.dirname(
    os.path.dirname(__file__)
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



# if __name__ == '__main__':

