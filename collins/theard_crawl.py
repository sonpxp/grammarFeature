import json
import re
import sqlite3
import threading
import urllib.parse
from threading import Thread
from time import sleep
from urllib.request import Request, urlopen
import continue_crawl_except as db

from bs4 import BeautifulSoup


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

        list_data = [None, None]

        try:
            title = str(soup.find('div', class_='title_container')
                        .find('h2', class_='h2_entry').find('span', class_='orth').text)
            span_parent = str(soup.find('span', class_='form inflected_forms type-infl'))

            list_data = [title, span_parent]
        except:
            return list_data

        return list_data

    @staticmethod
    def word_dict():
        words = json.load(open("../en.json", encoding="utf-8"))
        pattern = r"\w+"
        list_data = []
        for word in words:
            a = re.findall(pattern, str(word))
            list_data.extend(a)

        # Remove any duplicates from a List:
        list_data = list(dict.fromkeys(list_data))
        return list_data

    def save_collins_dict(self, spans: list):
        conn = sqlite3.connect('../collins.db')
        cursor = conn.cursor()
        try:
            table = """ CREATE TABLE IF NOT EXISTS COLLINS (
                                    query NVARCHAR(255) NOT NULL,
                                    word NVARCHAR(255),
                                    html TEXT
                                ); """
            cursor.execute(table)

            for query in spans:
                list_span = self.fetch(query)

                word = list_span[0]
                span = list_span[1]

                db_collins = "INSERT INTO COLLINS (query,word,html) values (?, ?, ?)"
                cursor.execute(db_collins, (query, word, span))
                conn.commit()

            conn.close()

        except sqlite3.Error as error:
            print("Failed to insert data into sqlite table: ", error)

    def requestHTML(self, data_words):
        sleep(0.2)
        self.save_collins_dict(data_words)

    @staticmethod
    def multithreading_crawl():
        # data = scraper.word_dict()
        data = db.square()

        parent_list = []
        # list này có 155k item
        # chia list này 20 list nhỏ, mỗi list 7k item và 1 list số dư còn lại

        for i in range(0, len(data), 7000):
            child_list = data[i:i + 7000]
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


if __name__ == '__main__':
    scraper = ElementsScraper()
    try:
        scraper.multithreading_crawl()
    except:
        scraper.multithreading_crawl()
