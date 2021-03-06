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
        web_byte = urlopen(req).read()
        webpage = web_byte.decode('utf-8')
        soup = BeautifulSoup(webpage, 'html.parser')

        try:
            title = soup.find('div', class_='title_container').find('h2', class_='h2_entry').find('span', class_='orth')
            grammars = soup.find('span', class_='form inflected_forms type-infl').find_all('span', class_='orth')
            span_tag = soup.find('span', class_='form inflected_forms type-infl').find_all('span')
            span_parent = soup.find('span', class_='form inflected_forms type-infl')

        except:
            return None

        print(f'title: {title.text}')

        list1 = []
        list2 = []
        list_c = []

        for span in span_tag:
            compile = re.match('(^<span class="lbl type-gram">)', str(span))
            if compile:
                a = span.text
                b = re.sub('\n', ' ', a)
                c = re.sub(',', '', b)
                d = c.strip()
                list_c.append(d)
                # print(f'Aa: {a}')
            else:
                b = ''.join(list_c)
                list1.append(b.strip())
                list_c.clear()
                # print(f'Bb: {span.text}')

        # Remove any duplicates from a List:
        list1 = list(dict.fromkeys(list1))

        # remote empty string from list
        list1 = list(filter(None, list1))

        # add data list 2:
        for grammar in grammars:
            a = grammar.text
            list2.append(a.strip())

        '''
        map 2 list -> 1 dict
        '''
        res = dict(zip(list1, list2))

        print(f'{q}: {res}')
        # return {q: res}
        return span_parent

    def word_dict(self):
        words = json.load(open("en.json", encoding="utf-8"))
        pattern = r"\w+"
        list_data = []
        for word in words:
            a = re.findall(pattern, word)

            # Use the extend() method to add list2 at the end of list1:
            # list1.extend(list2)
            list_data.extend(a)

        # Remove any duplicates from a List:
        list_data = list(dict.fromkeys(list_data))
        return list_data

    def requestHTML(self):
        pass
        # list_words = self.word_dict()
        # datas = []
        # for word in list_words:
        #     data = self.fetch(word)
        #     datas.append(data)
        # return datas


scraper = ElementsScraper()
scraper.fetch('big')

# if __name__ == '__main__':
#     scraper = ElementsScraper()
#     scraper.requestHTML()
