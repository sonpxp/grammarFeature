import threading
import time


def square(numbers):
    print('Calculator square of number: ')
    for x in numbers:
        time.sleep(1)
        print(f'Square: {x * x}')


def cube(numbers):
    print('Calculator cube of number: ')
    for x in numbers:
        time.sleep(1)
        print(f'Cube: {x * x * x}')


arr = [1, 3, 5, 6, 8]


t = time.time()
# square(arr)
# cube(arr)

thread_1 = threading.Thread(target=square, args=(arr,))
thread_2 = threading.Thread(target=cube, args=(arr,))

thread_1.start()
thread_2.start()

thread_1.join()
thread_2.join()

print('Done in: ', time.time() - t)
print('active_count: ', threading.active_count())
print('enumerate: ', threading.enumerate())
