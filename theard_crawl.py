import json
import re
import threading
import urllib.parse
from threading import Thread
from urllib.request import Request, urlopen

from bs4 import BeautifulSoup

import collin_db


class ElementsScraper:
    def __init__(self):
        self.list_data = None

    @staticmethod
    def fetch(q: str):
        url = 'https://www.collinsdictionary.com/dictionary/english/' + urllib.parse.quote(q)
        print(url)
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        web_byte = urlopen(req).read()
        webpage = web_byte.decode('utf-8')
        soup = BeautifulSoup(webpage, 'html.parser')

        try:
            span_parent = str(soup.find('span', class_='form inflected_forms type-infl'))

        except:
            return None

        return span_parent

    def word_dict(self):
        words = json.load(open("en.json", encoding="utf-8"))
        pattern = r"\w+"
        list_data = []
        for word in words:
            a = re.findall(pattern, str(word))
            list_data.extend(a)

        # Remove any duplicates from a List:
        list_data = list(dict.fromkeys(list_data))
        return list_data

    def requestHTML(self, data_words):
        for word in data_words:
            data = self.fetch(word)
            # save to db sqlite3
            collin_db.save_collins_dict_to_db(word, data)


if __name__ == '__main__':
    scraper = ElementsScraper()
    # scraper.requestHTML()

    data = scraper.word_dict()

    parent_list = []
    # list này có 155k item
    # chia list này 20 list nhỏ, mỗi list 7k item và 1 list số dư còn lại

    # square thread (155/2000 ~ 78-79 thread)
    for i in range(0, len(data), 2000):
        child_list = data[i:i + 2000]
        parent_list.append(child_list)

    # Start all threads.
    # Running 20 thread = len[parent_list]
    threads = []
    for n in range(0, len(parent_list)):
        try:
            th = Thread(target=scraper.requestHTML, args=(parent_list[n],))
            th.start()
            threads.append(th)
        except:
            continue
    print('active_count: ', threading.active_count())
    print('enumerate: ', threading.enumerate())

    # Wait all threads to finish.
    for th in threads:
        th.join()
        # print('Time finish: ', time.time() - time_delay)
