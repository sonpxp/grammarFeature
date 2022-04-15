#

import re
import json
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup


def req(q: str):
    url = 'https://www.oxfordlearnersdictionaries.com/definition/english/' + q + '_1'
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})

    web_byte = urlopen(req).read()
    webpage = web_byte.decode('utf-8')
    soup = BeautifulSoup(webpage, 'html.parser')

    try:
        tag = soup.find('div', class_='webtop')
        data = tag.find('div', class_='inflections')
        print(data.text)
    except:
        print('error')
        return


req('big')
# test case
# list_c = ['slow', 'dog', 'category', 'hongpeoi', 'entity']
# for c in list_c:
#     req(c)
#     print(req(c))
