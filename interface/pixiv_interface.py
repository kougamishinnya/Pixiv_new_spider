import requests
import json
import time
import math
from multiprocessing.dummy import Pool

from config.setting import *
from lib.get_ips import get_ips
from time import sleep

proxy = get_ips()  # proxt listをとる


def get_rank_id_list(date, number, mode, content=None):  # ランキングのイラストIDを獲得
    global img_path
    # URL引数の設定

    params_rank = {'mode': 'daily', 'content': 'illust', 'date': '', 'p': '1', 'format': 'json'}
    headers['referer'] = 'https://www.pixiv.net/ranking.php'
    params_rank['mode'] = mode
    if content is None:
        del params_rank['mode']
    else:
        params_rank['content'] = content
    params_rank['date'] = date
    page = math.ceil(number / 50)  # 1 ページがID50個あるので、ダウンロードしたい個数からページを計算
    illust_id_list = []
    for i in range(1, int(page) + 1):
        params_rank['p'] = str(page)
        try:
            url_get = requests.get(url=url_rank, headers=headers, proxies=random.choice(proxy),
                                   params=params_rank)
        except:
            print(f"Get {date} json_page {i} timeout")
        else:
            if url_get.status_code == 200:
                print(f"Get {date} json_page {i} successful")
                url_get = url_get.text
                url_json = json.loads(url_get)
                json_list = url_json['contents']
                for dict in json_list:
                    user_id = dict['illust_id']
                    number = int(number) - 1
                    illust_id_list.append(user_id)
                img_path = os.path.join(
                    PATH, 'Pixiv_img/rank', date
                )
                if not os.path.exists(img_path):
                    os.makedirs(img_path)
                    # if not os.path.exists(self.img_path):
                    #     os.mkdir(self.img_path)
                return illust_id_list[0:number]  # 戻り値はイラストIDリスト
            else:
                print(f"Get {date} json_page {i} Error")


def liked_user_illustlist(likedUser_id):
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
    if not os.path.exists(path):
        from lib.get_data import get_data
        cookie, user_id = get_data(likedUser_id)
        headers['cookie'] = cookie
        headers['x-user-id'] = user_id
        with open(path, 'w+') as f:
            data = {
                'cookie': cookie,
                'user_id': user_id
            }
            json.dump(data, f)
    else:
        with open(path, 'r') as f:
            config = json.load(f)
            headers['cookie'] = config['cookie']
            headers['x-user-id'] = config['user_id']

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


def get_original_url(illust_id):  # 引数はillust id
    original_url_list = []
    the_original_url = 'https://www.pixiv.net/ajax/illust/' + str(illust_id) + '/pages?lang=zh'  # json requests url
    try:  # request json data to get real pixiv_img url
        url_get = requests.get(url=the_original_url, headers=headers, proxies=random.choice(proxy),
                               timeout=1000)
    except:
        print("Get illust original_url json Error")
    else:
        if url_get.status_code == 200:
            url_get = url_get.text
            original_json = json.loads(url_get)
            for dict_urls in original_json['body']:
                original_url = dict_urls['urls']['original']
                original_url_list.append(original_url)
        else:
            print("Get illust original_url json load Error")
    return original_url_list  # 一つのID　URLは複数のイラストがあるかもしれないので、戻り値はオリジナルのイラストのリスト


def download_pic(url):  # 引数はオリジナルイラストのURL
    title = url.split('/')[-1]  # イラストの番号
    headers['referer'] = 'https://www.pixiv.net/ranking.php?mode=monthly'
    path = os.path.join(
        img_path, title
    )
    try:
        sleep(0.2)
        pic_get = requests.get(url=url, headers=headers,
                               proxies=random.choice(proxy))
        sleep(0.2)

    except:
        print(f"Original img.content download error")
    else:
        with open(path, 'wb') as fp:
            try:
                fp.write(pic_get.content)
                print(f"{title} saved")
            except:
                print(f'Img {title} save error')


def all_download(id_list):
    pool_num = 8
    pool = Pool(pool_num)  # poolを使う
    original_list = pool.map(get_original_url, id_list)  # マルチスレッド
    the_original_list = []
    max_num = int(input('Please enter the max of downloads one illust page\n---->'))
    for url_list in original_list:
        if len(url_list) > max_num:
            continue
        else:
            for ori_url in url_list:
                the_original_list.append(ori_url)
    pool.map(download_pic, the_original_list)  # マルチスレッド ダウンロード
    print(f"Illust download successful,downloads {len(the_original_list)} illusts")
    pool.close()  # Close pool
    pool.join()


# if __name__ == "__main__":
    # id_list = liked_user_illustlist('6662895')
    # print(id_list)
