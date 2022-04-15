import re
import json
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup


def req(q: str):
    url = 'https://www.collinsdictionary.com/dictionary/english/' + q
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})

    web_byte = urlopen(req).read()
    webpage = web_byte.decode('utf-8')
    soup = BeautifulSoup(webpage, 'html.parser')
    try:
        features = soup.find('span', class_='form inflected_forms type-infl').find_all('span', class_='lbl type-gram')
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
            c = b.strip()
            list_c.append(c)
            # print(f'AS: {a}')
            # print("compile completed")
        else:
            b = ''.join(list_c)
            list1.append(b.strip())
            list_c.clear()
            # print(f'Ab: {span.text}')

    # Remove any duplicates from a List:
    list1 = list(dict.fromkeys(list1))

    # remote empty string from list
    list1 = list(filter(None, list1))

    # for feature in features:
    #     a = feature.text
    #     # regex "\n"
    #     b = re.sub('\n', ' ', a)
    #     list1.append(b)
    #     # print(feature.text)
    #

    # add data list 2
    for grammar in grammars:
        a = grammar.text
        list2.append(a.strip())

    '''
    convert 2 list -> 1 dict
    '''
    res = dict(zip(list1, list2))

    # print(f'{q}: {res}')
    return {q: res}


# req("dog")

# test case
list_c = ['slow', 'dog', 'category', 'hongpeoi', 'entity']
for c in list_c:
    req(c)
    print(req(c))
