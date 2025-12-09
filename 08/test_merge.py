from loguru import logger

#Importing 
from queue import Queue
q = Queue(maxsize=2)
print("Initial size:", q.qsize())

q.put_nowait('a')
q.put_nowait('b')
q.put_nowait('c')
print(q)