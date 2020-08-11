from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ChromeOptions
from time import sleep
from config.setting import *
import re

path = os.path.dirname(
    os.path.dirname(__file__)
)

chrome_path = os.path.join(
    path, 'tools', 'chromedriver'
)

chrome_options = Options()  # Headless　設定
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')

option = ChromeOptions()  # Chromedriver の設定
option.add_experimental_option('excludeSwitches', ['enable-automation'])
bro = webdriver.Chrome(executable_path=chrome_path,
                       chrome_options=chrome_options, options=option)


# bro = webdriver.Chrome(executable_path=chrome_path, chrome_options = chrome_options)
# bro = webdriver.Chrome(executable_path=chrome_path)
def get_data(art_id):  # seleniumを使って、cookieをGET
    global username
    global password

    url = 'https://accounts.pixiv.net/login?return_to=https%3A%2F%2Fwww.pixiv.net%2Fen%2Fusers%2F' + art_id + '&lang=en&source=pc&view_type=page'
    bro.get(url)
    if username is None:
        username = str(input("Please enter your username\n---->"))
    if password is None:
        password = str(input("Please enter your password\n---->"))
    user_tag = bro.find_element_by_xpath(
        '//*[@id="LoginComponent"]/form/div[1]/div[1]/input')  # xpathでログインボタンを定位
    user_tag.send_keys(username)
    sleep(random.choice([0.2, 0.3, 0.4, 0.5]))
    pass_tag = bro.find_element_by_xpath('//*[@id="LoginComponent"]/form/div[1]/div[2]/input')
    pass_tag.send_keys(password)
    bro.find_element_by_xpath('//*[@id="LoginComponent"]/form/button').click()
    sleep(1)
    cookie_item = bro.get_cookies()  # Cookieを獲得
    print("Cookie get successful")
    cookie_str = ''
    page_text = bro.page_source
    ex = 'user_id: "(.*?)"'
    user_id = re.findall(ex, page_text, re.S)[0]
    print('UserID get successful')

    bro.quit()

    for item_cookie in cookie_item:  # dict cookie
        item_str = item_cookie["name"] + "=" + item_cookie["value"] + ";"
        cookie_str += item_str

    return cookie_str, user_id

