import time

time_start = time.time()

for i in range(1000000):
    print(i)

time_end = time.time()
print(time_end - time_start)