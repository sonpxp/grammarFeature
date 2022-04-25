import re

# using set() not index
t = [1, 2, 3, 1, 2, 3, 5, 6, 7, 8]
a = list(set(t))
# print(a)
# result: [1, 2, 3, 5, 6, 7, 8]


s = [1, 2, 3]
b = list(set(t) - set(s))
# print(b)
# result: [8, 5, 6, 7]

l1 = [1, 2, 6, 8]
l2 = [2, 3, 5, 8]
l3 = [x for x in l1 if x not in l2]
# print(f'l3: {l3}')

my_dict = {'plural, 3rd person singular presenttense': 'dogs', 'present participle': 'dogging',
           'past tense, past participle': 'dogged'}
gr = ['plural, 3rd person singular presenttense', 'present participle', 'past tense, past participle', 'superlative',
      'comparative']

stt = ['plural, 3rd person singular presenttense past tense, past participle', 'superlative', 'comparative', '3rd person singular presenttense past tense']

compiled = re.findall('(singular|plural|comparative|superlative)', str(stt))

pattern = r"\w+"


for i in range(len(stt)):
    d = re.findall(pattern, str(stt[i]))
    print(d)
    print(compiled[0])
    print("------------")


# for i in my_dict:
#     print(i, my_dict[i])
#
# new_list = []
# for i in gr:
#     # change key-dict
#     # dictionary[new_key] = dictionary[old_key]
#     mm = re.findall('plural', i)
#     cc = re.findall('comparative', i)
#     vv = re.findall('superlative', i)
#     if mm is not None:
#         new_list.append(mm)
#         print(mm)
#     if cc is not None:
#         new_list.append(cc)
#         print(cc)
#     if vv is not None:
#         new_list.append(vv)
#         print(vv)
# print(new_list)

# res = {'plural': 'consortiums', 'consortia': 'kənˈsɔːtiə', 'kənˈsɔːʃə': 'kənˈsɔːrtiə', 'comparative': 'grottier',
#        'superlative': 'grottiest'}
#
# dict_list = {}
# for k, v in res.items():
#     if k == 'plural' or k == 'comparative' or k == 'superlative' or k == 'singular':
#         dict_list.update({k: v})
# print(dict_list)

