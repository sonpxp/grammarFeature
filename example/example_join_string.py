lista = ['hello', 'join']
listb = ['mina']

listc = []
a = ', '.join(lista)
listc.append(a)
lista.extend(listb)

# print(lista)
# print(listc)
# print(' '.join(listc))

b = u'bats\u00E0'
# a = u' '.join(b).encode('utf-8').strip()

print(b)