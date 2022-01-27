# choose the linkpage with any following goods (not GPU necessary) on DNS-SHOP.RU and fun!
# when
# get link into URL variable
# login-pass : nigav.troikos@mrha.win password

import time
import random
from bs4 import BeautifulSoup as BS
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import winsound

url = 'https://www.dns-shop.ru/catalog/17a89aab16404e77/videokarty/?f[mx]=2ff-2fi&f[19n]=c0k&fr[vf]=65-129'
db_file = "C:\PyCharm_Projects\DNS_shop_parser\Test_db.txt"
product = '3050'  # the short str expression which can precisely identify good which you needed from list of all goods.

# this block can be used as is, no need to correct
list_of_goods_class = "catalog-products view-simple"
name_class = 'catalog-product__name ui-link ui-link_black'
price_class = 'product-buy__price-wrap product-buy__price-wrap_interactive'

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
}


def get_options():
    chrome_options = Options()
    chrome_options.add_argument(f"user-agent={headers['User-Agent']}")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--proxy-server='direct://'")
    chrome_options.add_argument("--proxy-bypass-list=*")
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument("--dns-prefetch-disable")
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--start-maximized')
    return chrome_options


def get_site():
    html = browser.get(url=url)
    soup = BS(browser.page_source, 'lxml')
    time.sleep(1)  # for better performance  browser.implicitly_wait() can be used
    products = soup.find_all(class_=list_of_goods_class)
    final_item_list = list()  # create list for data recording which will put it into database later.

    for item in products:
        gpu = item.find_all(class_=name_class)
        gpu_price = item.find_all(class_=price_class)

        if len(gpu_price) != len(gpu):  # in case of no server response
            gpu_price = ['no response'] * len(gpu)
            for i in range(len(gpu)):
                final_item_list.append((time.asctime(time.localtime()), gpu[i].text, gpu_price[i]))
        else:
            for i in range(len(gpu)):
                final_item_list.append((time.asctime(time.localtime()), gpu[i].text, gpu_price[i].text))

    for y in final_item_list:
        if product in str(y):
            for w in range(5):
                winsound.Beep(500, 1000)  # sound notification if good is appear on site and in available now.
                time.sleep(0.1)

    return final_item_list


def get_info(html):
    soup = BS(html, 'lxml')
    events = soup.find_all(class_=list_of_goods_class)
    print(soup)


def record_to_db(record_data):
    with open(db_file, 'a', encoding='utf-8') as file:
        for x in record_data:
            file.write(str(x) + '\n')


if __name__ == "__main__":
    chrome_options = get_options()
    browser = webdriver.Chrome(options=chrome_options)
    time.sleep(30)  # time for login:password on DNS-SHOP.RU

    while True:
        record_to_db(get_site())
        time.sleep(random.randint(9, 12))  # select pseudo-random number for timeout before the next request