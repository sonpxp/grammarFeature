import re
import sqlite3
from queue import Empty
import json
from bs4 import BeautifulSoup


class MultiThreadedCrawler:

    @staticmethod
    def select_db_collins() -> list:
        conn = sqlite3.connect('../collins.db')
        cursor = conn.cursor()
        try:

            grammar = []
            # html_db = cursor.execute('''SELECT word,html FROM COLLINS GROUP BY word LIMIT 3000''')
            html_db = cursor.execute('''SELECT word,html FROM COLLINS GROUP BY word''')

            for html in html_db:
                a = list(html)
                grammar.append(a)
            return grammar

        except sqlite3.Error as error:
            print("Failed to select data table: ", error)

    @staticmethod
    def parse_links(html):
        soup = BeautifulSoup(html, 'html.parser')
        try:
            grammars = soup.find('span', class_='form inflected_forms type-infl').find_all('span', class_='orth')
            span_tag = soup.find('span', class_='form inflected_forms type-infl').find_all('span')

        except:
            return None

        grammar_feature = []
        grammar_content = []

        list_c = []

        for span in span_tag:
            compile = re.match('(^<span class="lbl type-gram">)', str(span))
            if compile:
                a = span.text
                b = re.sub('\n', ' ', a)
                c = re.sub(',', '', b)
                d = c.strip()
                list_c.append(d)

            else:
                b = ', '.join(list_c)
                grammar_feature.append(b.strip())
                list_c.clear()

        # Remove any duplicates from a List:
        grammar_feature = list(dict.fromkeys(grammar_feature))

        # remote empty string from list
        grammar_feature = list(filter(None, grammar_feature))

        for g in range(len(grammar_feature)):
            compiled = re.findall('(^plural|^comparative|^superlative|^singular)', str(grammar_feature[g].strip()))
            # print(compiled)
            if compiled:
                grammar_feature[g] = compiled[0]
            else:
                pass

        # add data list 2:
        for grammar in grammars:
            a = grammar.text
            grammar_content.append(str(a).strip())

        '''
        map 2 list -> 1 dict
        '''

        if len(grammar_feature) == len(grammar_content):

            res = dict(zip(grammar_feature, grammar_content))
            dict_list = {}
            for k, v in res.items():
                if k == 'plural' or k == 'comparative' or k == 'superlative' or k == 'singular':
                    dict_list.update({k: v})
            print(dict_list)
            return dict_list
        else:
            return None

    def save_new_db(self):
        db_dict = self.select_db_collins()

        # test case
        # db_dict = ['dizzy', 'dull', 'love', 'faint', 'fast']

        conn = sqlite3.connect('../collins_dict.db')
        cursor = conn.cursor()
        try:
            table = """ CREATE TABLE IF NOT EXISTS collins_dict (
                                        word NVARCHAR(255) NOT NULL,
                                        content TEXT
                                    ); """
            cursor.execute(table)

            for i in db_dict:
                word = i[0]
                content = self.parse_links(str(i[1]))
                print(f'word: {word}, content: {content}')
                print(f'--------------')
                # content = self.parse_links()

                db_collins = "INSERT INTO collins_dict (word,content) values (?, ?)"
                cursor.execute(db_collins, (str(word), json.dumps(content, ensure_ascii=False)))
                conn.commit()
            conn.close()

        except sqlite3.Error as error:
            print("Failed to insert data into sqlite table: ", error)

    @staticmethod
    def run_web_crawler():
        while True:
            try:
                pass

            except Empty:
                return
            except Exception as e:
                print(e)
                continue


a = MultiThreadedCrawler()
a.save_new_db()
