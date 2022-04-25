#
import re
import sqlite3
import urllib.parse
from threading import Thread
from time import sleep
from urllib.request import Request, urlopen

from bs4 import BeautifulSoup

from collins.continue_crawl_except import word_dict


class OxfordScraper:

    @staticmethod
    def fetch(q: str):
        url = 'https://www.oxfordlearnersdictionaries.com/definition/english/' + urllib.parse.quote(q)
        print(url)
        target_url = Request(url, headers={'User-Agent': 'Mozilla/5.0'})

        l1 = []
        l2 = []
        l3 = [None, None]

        try:
            web_byte = urlopen(target_url).read()
            webpage = web_byte.decode('utf-8')
            soup = BeautifulSoup(webpage, 'html.parser')

            word = soup.find(name='h1', class_='headword')
            tag = soup.find('div', class_='webtop')

            data = tag.find('div', class_='inflections')
            inflected = tag.find_all('span', class_='inflected_form')

            a = data.text
            b = a.split()


            # print(f'b: {b}')
            # print(f'inflected: {inflected}')


            # list_c = []
            # for i in inflected:
            #     list_c.append(i.text)
            #     print(f'inflected: {i.text}')
            #
            # print(f'list_c: {list_c}')

            pattern = r"\w+"

            # for i in range(len(b)):
            #     if (i % 2) == 0:
            #         key = re.findall(pattern, str(b[i]))
            #         l1.extend(key)
            #     else:
            #         value = re.findall(pattern, str(b[i]))
            #         l2.extend(value)

            list_d = []

            for i in b:
                regex = re.findall('($,)', str(i))
                if i == 'plural' or i == 'comparative' or i == 'superlative' or i == 'singular':
                    l1.append(i)
                else:
                    if regex:
                        pass


                print(i)
                print('--------')

            # assert l1 == l2

            print(f'l1: {l1}')
            print(f'l2: {l2}')

            res = dict(zip(l1, l2))
            dict_list = {}
            for k, v in res.items():
                if k == 'plural' or k == 'comparative' or k == 'superlative' or k == 'singular':
                    dict_list.update({k: v})

            word_db = word.text.strip()

            l3.append(word_db)
            l3.append(res)

            # return res
            l3 = [word_db, str(dict_list)]

        except:
            print("ex: Error")
            l3 = [q, None]
            return l3

        print(f'l3: {l3}')
        return l3

    def save_oxford_dict(self, spans: list):
        conn = sqlite3.connect('../oxford.db')
        cursor = conn.cursor()
        try:
            table = """ CREATE TABLE IF NOT EXISTS OXFORD (
                                        query NVARCHAR(255) NOT NULL,
                                        word NVARCHAR(255),
                                        content TEXT
                                    ); """
            cursor.execute(table)

            for query in spans:
                list_span = self.fetch(query)

                word = list_span[0]
                content = str(list_span[1])

                print(f'word: {word}')
                print(f'content: {content}')

                db_oxford = "INSERT INTO OXFORD (query,word,content) values (?, ?, ?)"
                cursor.execute(db_oxford, (query, word, content))
                conn.commit()

            conn.close()

        except sqlite3.Error as error:
            print("Failed to insert data into sqlite table: ", error)

    def requestHTML(self, data_words):
        sleep(0.5)
        self.save_oxford_dict(data_words)

    def run_web_crawler(self):
        data = word_dict()
        parent_list = []
        # list này có 155k item
        # chia list này 20 list nhỏ

        for i in range(0, len(data), len(data) // 20):
            child_list = data[i:i + len(data) // 20]
            parent_list.append(child_list)

        # Start all threads.
        # Running 20 thread = len[parent_list]
        threads = []
        for n in range(0, len(parent_list)):
            try:
                th = Thread(target=self.requestHTML, args=(parent_list[n],))
                th.start()
                threads.append(th)
            except:
                continue

        # Wait all threads to finish.
        for th in threads:
            th.join()


# test case
list_c = ['slow', 'coccyx']
# list_c = ['slow', 'coccyx', 'dog', 'category', 'hongpeoi', 'entity']
scraper = OxfordScraper()
for c in list_c:
    try:
        scraper.fetch(c)
    except:
        continue

# scraper = OxfordScraper()
# scraper.run_web_crawler()
#scraper.save_oxford_dict(list_c)
