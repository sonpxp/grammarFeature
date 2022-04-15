import json
import re
import urllib.parse
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
            title = soup.find('div', class_='title_container').find('h2', class_='h2_entry').find('span', class_='orth')
            grammars = soup.find('span', class_='form inflected_forms type-infl').find_all('span', class_='orth')
            span_tag = soup.find('span', class_='form inflected_forms type-infl').find_all('span')
            span_parent = str(soup.find('span', class_='form inflected_forms type-infl'))

        except:
            return None

        list1 = []
        list2 = []
        list_c = []

        # print(soup.find('span', class_='form inflected_forms type-infl'))
        # print(f'title: {title.text}')

        # for span in span_tag:
        #     compile = re.match('(^<span class="lbl type-gram">)', str(span))
        #     if compile:
        #         a = span.text
        #         b = re.sub('\n', ' ', a)
        #         c = re.sub(',', '', b)
        #         d = c.strip()
        #         list_c.append(d)
        #         # print(f'AS: {a}')
        #     else:
        #         b = ''.join(list_c)
        #         list1.append(b.strip())
        #         list_c.clear()
        #         # print(f'Ab: {span.text}')
        #
        # # Remove any duplicates from a List:
        # list1 = list(dict.fromkeys(list1))
        #
        # # remote empty string from list
        # list1 = list(filter(None, list1))
        #
        # # add data list 2:
        # for grammar in grammars:
        #     a = grammar.text
        #     list2.append(a.strip())

        '''
        map 2 list -> 1 dict
        '''
        res = dict(zip(list1, list2))

        # print(f'{q}: {res}')
        # return {q: res}
        return span_parent

    def word_dict(self):
        words = json.load(open("en.json", encoding="utf-8"))
        pattern = r"\w+"
        list_data = []
        for word in words:
            # for word in list_c:
            a = re.findall(pattern, str(word))
            # list_data.append(a)

            # Use the extend() method to add list2 at the end of list1:
            # list1.extend(list2)
            list_data.extend(a)

        # Remove any duplicates from a List:
        list_data = list(dict.fromkeys(list_data))
        return list_data

    def requestHTML(self):
        list_words = self.word_dict()
        datas = []
        for word in list_words:
            data = self.fetch(word[2169::])
            # datas.append(data)
            # save to db sqlite3
            collin_db.save_collins_dict_to_db(word, data)
        return datas


if __name__ == '__main__':
    scraper = ElementsScraper()
    scraper.requestHTML()
