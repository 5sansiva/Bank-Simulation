#!/usr/bin/env python3

import threading
import random
import time
from queue import Queue

teller_semaphore = threading.Semaphore(3)
teller_ready_barrier = threading.Barrier(3)

waiting_customers = Queue()

class Teller(threading.Thread):
    def __init__(self, teller_id, safe_sem, manager_sem, customer_queue):
        super().__init__()
        self.teller_id = teller_id
        self.safe_sem = safe_sem
        self.manager_sem = manager_sem
        self.customer_queue = customer_queue

    def run(self):
        print(f"Teller {self.teller_id} [Teller {self.teller_id}]: ready to serve")
        teller_ready_barrier.wait()
        while True:
            customer = self.customer_queue.get()
            if customer is None:
                print(f"Teller {self.teller_id} [Teller {self.teller_id}]: received shutdown signal.")
                break

            print(f"Teller {self.teller_id} [Teller {self.teller_id}]: is serving Customer {customer.customer_id}")
            customer.start_service(self)

            if customer.transaction == "Withdraw":
                print(f"Teller {self.teller_id} [Teller {self.teller_id}]: requesting manager permission")
                with self.manager_sem:
                    print(f"Teller {self.teller_id} [Teller {self.teller_id}]: interacting with manager")
                    time.sleep(random.uniform(0.005, 0.03))
                    print(f"Teller {self.teller_id} [Teller {self.teller_id}]: done with manager")

            print(f"Teller {self.teller_id} [Teller {self.teller_id}]: going to safe")
            with self.safe_sem:
                print(f"Teller {self.teller_id} [Teller {self.teller_id}]: in the safe")
                time.sleep(random.uniform(0.01, 0.05))
                print(f"Teller {self.teller_id} [Teller {self.teller_id}]: leaving the safe")

            print(f"Teller {self.teller_id} [Teller {self.teller_id}]: done with Customer {customer.customer_id}")
            customer.end_service()


class Customer(threading.Thread):
    def __init__(self, customer_id, entry_sem, customer_queue):
        super().__init__()
        self.customer_id = customer_id
        self.entry_sem = entry_sem
        self.customer_queue = customer_queue
        self.transaction = random.choice(["Deposit", "Withdraw"])
        self.service_done = threading.Event()

    def run(self):
        time.sleep(random.uniform(0, 0.1))  # wait 0–100 ms
        with self.entry_sem:
            print(f"Customer {self.customer_id} [Customer {self.customer_id}]: enters bank to {self.transaction}")
            self.customer_queue.put(self)
            self.service_done.wait()
            print(f"Customer {self.customer_id} [Customer {self.customer_id}]: transaction complete, exiting")

    def start_service(self, teller):
        print(f"Customer {self.customer_id} [Customer {self.customer_id}]: starts with Teller {teller.teller_id}")

    def end_service(self):
        self.service_done.set()

if __name__ == "__main__":
    numCustomers = 10
    numTellers = 3

    entry = threading.Semaphore(2)
    safe = threading.Semaphore(2)
    manager = threading.Semaphore(1)
    teller_ready_barrier = threading.Barrier(numTellers)
    customerQueue = Queue()


    tellers = [Teller(i, safe, manager, customerQueue) for i in range(numTellers)]
    for t in tellers:
        t.start()

    customers = [Customer(i, entry, customerQueue) for i in range(numCustomers)]
    for c in customers:
        c.start()
    
    for c in customers:
        c.join()
    for _ in range(numTellers):
        customerQueue.put(None)
    for t in tellers:
        t.join()
