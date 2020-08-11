import requests
import json
import time
from lxml import etree
import re
from config.setting import *


# global username
# global password
#
# path = os.path.dirname(
#     os.path.dirname(__file__)
# )
#
# # path = os.path.join(
# #     path, 'tools'
# # )
# # sys.path.append(path)
# chrome_path = os.path.join(
#     path, 'tools', 'chromedriver'
# )
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


proxy = get_ips()


def get_id(likedUser_id):
    global img_path
    likedUser_id = str(likedUser_id)
    illust_id_list = []
    # headers['sec-fetch-site']= 'same-origin'
    # headers['sec-fetch-mode'] = 'cors'
    # headers['sec-fetch-dest'] = 'empty'
    '''
    ここはログインが必要だから、get_cookieを使う、そして、x-user-idは自分のアカウントのID
    もう一つ重要な引数はreferer,これはこのrequestsするページの前のページです
    '''
    start_time = time.time()
    user_id = '15691732'
    c2 = open('cookie795196.txt', 'r')
    c2_text = c2.read()
    headers['cookie'] = ''
    headers['x-user-id'] = user_id
    headers['referer'] = 'https://www.pixiv.net/users/' + likedUser_id
    json_url = 'https://www.pixiv.net/ajax/user/' + likedUser_id + '/profile/all?lang=en'
    try:
        json_load = requests.get(url=json_url, headers=headers, proxies=random.choice(proxy))
    except:
        print('Get user illust list Error')
    else:
        if json_load.status_code == 200:
            json_text = json.loads(json_load.text)
            for value in json_text['body']['illusts']:
                illust_id_list.append(value)
            global img_path
            img_path = os.path.join(
                PATH, 'Pixiv_img/user', likedUser_id
            )
            if not os.path.exists(img_path):
                os.makedirs(img_path)
            end_time = time.time()
            print(
                f"Geted {len(illust_id_list)} illust id of artist_id : {likedUser_id}\nIt took {end_time - start_time} seconds")
            return illust_id_list  # id list
        else:
            print("Get liked user illust list Error")


def login(cookie,username,password):
    pass



if __name__ == '__main__':


    path = os.path.dirname(
        os.path.dirname(__file__)
    )

    db_path = os.path.join(
        path, 'config','config.json'
    )
    # print(db_path)
    # proxy = get_ips()
    # from lib import common
    # art_id = '6662895'
    # cookie, user_id = common.get_data(art_id)
    # with open(db_path, 'w') as f:
    #     json.dump(data, f)
    # img_list = get_id('6662895')
    # print(img_list)
    print(db_path)



    # if len(img_list) == 142:
    #     print('cookie通用')
    # else:
    #     print('不通用')
    # print(len(img_list))
