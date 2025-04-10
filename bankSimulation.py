#!/usr/bin/env python3

import threading
import random
import time
from queue import Queue

teller_semaphore = threading.Semaphore(2)


waiting_customers = Queue()

def customer_behavior(customer_id, customer_sem):
    print(f"Customer {customer_id} arrives and waits.")
    waiting_customers.put((customer_id, customer_sem))
    customer_sem.acquire()  # Wait to be called by a teller
    print(f"Customer {customer_id} is being served.")
    time.sleep(random.uniform(1, 3))  # Simulate time with the teller
    print(f"Customer {customer_id} is done and leaves.")

def teller_behavior(teller_id):
    while True:
        teller_semaphore.acquire()  # Wait until a teller is free
        customer_id, customer_sem = waiting_customers.get()  # Serve the next customer
        print(f"Teller {teller_id} is serving Customer {customer_id}.")
        customer_sem.release()  # Let the customer proceed
        time.sleep(random.uniform(1, 2))  # Simulate teller processing time
        print(f"Teller {teller_id} finished with Customer {customer_id}.")
        teller_semaphore.release()


# Start tellers
for i in range(2):
    threading.Thread(target=teller_behavior, args=(i,), daemon=True).start()

# Start customers
for i in range(10):
    cust_sem = threading.Semaphore(0)
    threading.Thread(target=customer_behavior, args=(i, cust_sem)).start()
    time.sleep(random.uniform(0.1, 0.5))  # Stagger customer arrivals
