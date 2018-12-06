import threading
import time

def thread_target():
    i = 1
    while True:
        print(i)
        time.sleep(1)


flag = True
thread_obj = threading.Thread(target = thread_target)
thread_obj.start()
thread_obj.join(timeout = 5)
flag = False