import json
import re
import time

import requests
from bs4 import BeautifulSoup


class ElementsScraper:
    base_url = 'http://tratu.coviet.vn/hoc-tieng-anh/cau-truc-cau-tieng-anh-thong-dung/vietgle-tra-tu/tat-ca/trang-'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36 Edg/95.0.1020.40'}

    @staticmethod
    def fetch(url):
        print('HTTP GET request to URL: %s' % url, end='')
        response = requests.get(url)
        print(' | Status code: %s' % response.status_code)
        return response

    @staticmethod
    def upper_char(str):
        return re.sub("(^|[.?!])\s*(.)", lambda p: p.group(0).upper(), str)

    def parse(self, html):
        content = BeautifulSoup(html, 'html.parser')
        datas = content.find_all('ul', {'class': 'ucttatd ovf'})
        english_phrases = []

        for data in datas:
            item_phrase = {}
            example = []

            phrase_1 = data.find('span', class_='ctk').text
            mean_1 = data.find('span', class_='p5l cB').text

            match_en = re.findall(r'<li class="icham m5t ctk".*?>(.*?)<\/li>', str(data))
            match_vi = re.findall(r'<li class="p10l".*?>(.*?)<\/li>', str(data))
            assert len(match_vi) == len(match_en)

            phrase = self.upper_char(phrase_1)
            mean = self.upper_char(mean_1.replace(";", ","))

            for i in range(len(match_vi)):
                example.append({"en": match_en[i], "vi": match_vi[i]})

            item_phrase["phrase"] = phrase
            item_phrase["mean"] = mean
            item_phrase["example"] = example

            english_phrases.append(item_phrase)

        return english_phrases

    @staticmethod
    def to_json(item):
        with open('../database/data_english_phrases.json', 'w', encoding='utf-8') as f:
            json.dump(item, f, ensure_ascii=False, indent=4)

    def run(self):
        new_data = []
        for page in range(1, 128):
            next_page = self.base_url + str(page) + ".html"
            response = self.fetch(next_page)

            if response.status_code == 200:
                # self.parse(response.text)
                new_data += self.parse(response.text)
            else:
                print('Something has gone wrong, skiping to next page')
                continue
            # time.sleep(2)  # second

        return self.to_json(new_data)


if __name__ == '__main__':
    scraper = ElementsScraper()
    scraper.run()
