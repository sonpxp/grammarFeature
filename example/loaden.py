import re
import json

# my_string = "Let's write RegEx!"
# PATTERN = r"\w+"
# re.findall(PATTERN, my_string)

words = json.load(open("../en.json", encoding="utf8"))

my_string = "Let's write RegEx!"
PATTERN = r"\w+"

listData = []
for word in words:
    a = re.findall(PATTERN, word)
    # listData.append(a)

    # Use the extend() method to add list2 at the end of list1:
    # list1.extend(list2)
    listData.extend(a)

print(len(listData))

# Remove any duplicates from a List:
listData = list(dict.fromkeys(listData))
print(len(listData))
# print(listData)
