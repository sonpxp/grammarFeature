import json
import re
from urllib.request import Request, urlopen

from bs4 import BeautifulSoup


class ElementsScraper:
    def __init__(self):
        self.list_data = None

    @staticmethod
    def fetch(q: str):
        url = 'https://www.collinsdictionary.com/dictionary/english/' + q
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        web_byte = urlopen(req, timeout=10).read()
        webpage = web_byte.decode('utf-8')
        soup = BeautifulSoup(webpage, 'html.parser')

        try:
            features = soup.find('span', class_='form inflected_forms type-infl').find_all('span',class_='lbl type-gram')
            grammars = soup.find('span', class_='form inflected_forms type-infl').find_all('span', class_='orth')
            span_tag = soup.find('span', class_='form inflected_forms type-infl').find_all('span')
        except:
            return {q: None}

        list1 = []
        list2 = []

        list_c = []

        for span in span_tag:
            compile = re.match('(^<span class="lbl type-gram">)', str(span))
            if compile:
                a = span.text
                b = re.sub('\n', ' ', a)
                c = re.sub(',', '', b)
                d = b.strip()
                list_c.append(d)
                # print(f'AS: {a}')
                # print("compile completed")
            else:
                b = ''.join(list_c)
                list1.append(b.strip())
                list_c.clear()
                # print(f'Ab: {span.text}')

        list1 = list(dict.fromkeys(list1))

        # remote empty string from list
        list1 = list(filter(None, list1))
        # print(list1)

        for grammar in grammars:
            a = grammar.text
            list2.append(a.strip())

        # print(list2)

        '''
        map 2 list -> 1 dict
        '''
        # assert len(list1) == len(list2)
        res = dict(zip(list1, list2))

        print(f'{q}: {res}')
        # return {q: res}

    def word_dict(self):
        words = json.load(open("en.json", encoding="utf8"))
        pattern = r"\w+"
        list_data = []
        for word in words:
            a = re.findall(pattern, word)
            # list_data.append(a)

            # Use the extend() method to add list2 at the end of list1:
            # list1.extend(list2)
            list_data.extend(a)

        # print(len(list_data))

        # Remove any duplicates from a List:
        list_data = list(dict.fromkeys(list_data))
        # print(len(list_data))
        # print(list_data)
        return list_data

    def requestHTML(self):
        list_words = self.word_dict()
        datas = []
        for word in list_words:
            data = self.fetch(word)
            datas.append(data)
            print(data)
        return datas


if __name__ == '__main__':
    scraper = ElementsScraper()
    scraper.requestHTML()
