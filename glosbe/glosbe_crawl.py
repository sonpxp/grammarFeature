import urllib.parse
from urllib.request import Request, urlopen

from bs4 import BeautifulSoup


def req(q: str):
    url = 'https://glosbe.com/en/en/' + urllib.parse.quote(q)
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})

    web_byte = urlopen(req).read()
    webpage = web_byte.decode('utf-8')
    soup = BeautifulSoup(webpage, 'html.parser')
    try:
        # parent = soup.find('ul', class_='text-xs grammar-tables').find_all('li', class_='pl-4 mb-2 overflow-x-auto')
        parent = soup.find_all('li', class_='pl-4 mb-2 overflow-x-auto')
    except:
        return

    # print(parent)

    list1 = []

    for i in parent:
        try:
            print(i.text)
            item = i.text
            list1.append(item)
            # titles = i.find('i').text
            # grammars = i.find('b').text
            # b = {q: {titles: grammars}}
            # print(b)
            #
            # return b
        except:
            continue

        # Remove any duplicates from a List:
    list1 = list(dict.fromkeys(list1))
    print(list1)
    return list1


req('big')

# test case
# list_c = ['employ', 'slow', 'dog', 'category', 'hongpeoi', 'entity']
# for c in list_c:
#     req(c)
#     print(req(c))
