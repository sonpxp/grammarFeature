from threading import *
import time


# class Hello():
#     def run(self):
#         for i in range(10):
#             time.sleep(1)
#             print("Hello")
#
#
# class Hi():
#     def run(self):
#         for i in range(5):
#             time.sleep(2)
#             print("HI")


# t = time.time()
#
# t1 = Hello()
# t2 = Hi()

# t1.run()
# t2.run()
#
# print('time finish: ', time.time() - t)  # print ~ 20s


# -------------------------------
# using thread

class Hello(Thread):
    def run(self):
        for i in range(10):
            time.sleep(1)
            print("td-Hello")


class Hi(Thread):
    def run(self):
        for i in range(5):
            time.sleep(2)
            print("td-HI")


t = time.time()

t1 = Hello()
t2 = Hi()

t1.start()
t2.start()

t1.join()
t2.join()

print('time finish: ', time.time() - t)
