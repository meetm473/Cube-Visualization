import threading
import time

start = time.perf_counter()

def do_something():
    print('\nSleeping for 1 second')
    time.sleep(1)
    print('\nDone sleeping')

t1 = threading.Thread(target=do_something)
t2 = threading.Thread(target=do_something)

t1.start()
t2.start()

t1.join()
t2.join()

finish = time.perf_counter()

print(f'\nFinished in {round(finish-start, 2)} seconds')
 
