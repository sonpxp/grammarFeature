lista = ['hello', 'join']
listb = ['mina']

listc = []
a = ', '.join(lista)
listc.append(a)
lista.extend(listb)

print(lista)
print(listc)
print(' '.join(listc))