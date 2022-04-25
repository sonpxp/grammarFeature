import json
import re
import sqlite3


# 155k dict
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


# query word in sqlite
def remote_list_duplicate_in_sqlite() -> list:
    global data
    conn = sqlite3.connect('../collins.db')
    cursor = conn.cursor()
    try:
        new_list = []
        data = cursor.execute('''SELECT query FROM COLLINS''')
        pattern = r"\w+"

        for word in data:
            a = re.findall(pattern, str(word))
            new_list.extend(a)
        # print(new_list)
        return new_list
        # conn.close()

    except sqlite3.Error as error:
        print("Failed to insert data into sqlite table: ", error)


# so word con lai chua dc query
def square() -> list:
    l1 = word_dict()
    l2 = remote_list_duplicate_in_sqlite()

    l3 = list(set(l1) - set(list(l2)))
    # l3 = [x for x in l1 if x not in l2]
    print(len(l1))
    print(len(l2))
    print(len(l3))
    return l3


square()
