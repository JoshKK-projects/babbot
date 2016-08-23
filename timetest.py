import time
start_time = time.time()
import config
r = config.r
for i in range(1,10000):
    getted = r.get('Ryan_user.txt_mainchains')
print time.time() - start_time

start_time = time.time()
key = r.get('Ryan_user.txt_mainchains')
for i in range(1,10000):
    dosoemthing = key
print time.time() - start_time