import time
from threading import Thread
from time import sleep

list_num = [1, 2, 3, 4, 5, 6, 7, 78, 8, 4, 5, 5, 6 , 6, 6, 6, 23, 6, 7, 8, 9, 9, 9, 4, 22, 44, 5, 6, 2312, 7, 88, 9, 242,
            3, 4, 4323, 4, 55, 232, 34343, 456, 453, 3, 4534, 564, 56, 77, 47, 4, 5, 45, 45, 5, 5, 5, 6]

sum_list = []
for i in range(0, len(list_num), 10):
    chunk = list_num[i:i + 10]
    sum_list.append(chunk)


def sum(Num):
    for n in Num:
        sleep(1)
        print("square:", n * n)


time_delay = time.time()

for i in sum_list:
    print(sum(i))
    print('Time finish: ', time.time() - time_delay)

# Start all threads.
threads = []
for n in range(0, len(sum_list)):
    th = Thread(target=sum, args=(sum_list[n],))
    th.start()
    threads.append(th)

# Wait all threads to finish.
for th in threads:
    th.join()
    print('Time finish: ', time.time() - time_delay)
