#!/usr/bin/env python3

import threading
import random
import time
from queue import Queue

class Teller(threading.Thread):
    def __init__(self, id, safe, manager, customerQueue):
        super().__init__()
        self.id = id
        self.safe = safe
        self.manager = manager
        self.customerQueue = customerQueue

    def run(self):
        print(f"Teller {self.id} []: ready to serve")
        print(f"Teller {self.id} []: waiting for a customer")
        
        teller_ready_barrier.wait()

        while True:
            customer = self.customerQueue.get()
            if customer is None:
                print(f"Teller {self.id} []: leaving for the day")
                break

            customer.selects_teller(self)
            customer.ready_for_transaction.wait()

            print(f"Teller {self.id} [Customer {customer.id}]: serving a customer")
            print(f"Teller {self.id} [Customer {customer.id}]: asks for transaction")
            transaction_type = customer.give_transaction(self)

            print(f"Teller {self.id} [Customer {customer.id}]: handling {transaction_type.lower()} transaction")

            if transaction_type == "Withdrawal":
                print(f"Teller {self.id} [Customer {customer.id}]: going to the manager")
                self.manager.acquire()
                print(f"Teller {self.id} [Customer {customer.id}]: getting manager's permission")
                time.sleep(random.uniform(0.005, 0.030))
                print(f"Teller {self.id} [Customer {customer.id}]: got manager's permission")
                self.manager.release()

            print(f"Teller {self.id} [Customer {customer.id}]: going to safe")
            self.safe.acquire()
            print(f"Teller {self.id} [Customer {customer.id}]: enter safe")
            time.sleep(random.uniform(0.010, 0.050))
            print(f"Teller {self.id} [Customer {customer.id}]: leaving safe")
            print(f"Teller {self.id} [Customer {customer.id}]: finishes {transaction_type.lower()} transaction.")
            self.safe.release()

            print(f"Teller {self.id} [Customer {customer.id}]: wait for customer to leave.")
            customer.finish_interaction(self)

class Customer(threading.Thread):
    def __init__(self, id, entry_semaphore, customerQueue):
        super().__init__()
        self.id = id
        self.entry_semaphore = entry_semaphore
        self.customerQueue = customerQueue
        self.transaction_type = random.choice(["Deposit", "Withdrawal"])
        self.teller = None
        self.teller_ready = threading.Event()
        self.transaction_done = threading.Event()
        self.ready_for_transaction = threading.Event()

    def run(self):
        print(f"Customer {self.id} []: wants to perform a {self.transaction_type.lower()} transaction")
        time.sleep(random.uniform(0, 0.1))  

        print(f"Customer {self.id} []: going to bank.")
        with self.entry_semaphore:  
            print(f"Customer {self.id} []: entering bank.")
            print(f"Customer {self.id} []: getting in line.")
            
            self.customerQueue.put(self)
            self.teller_ready.wait()  

            print(f"Customer {self.id} []: selecting a teller.")
            print(f"Customer {self.id} [Teller {self.teller.id}]: selects teller")
            print(f"Customer {self.id} [Teller {self.teller.id}] introduces itself")

            self.ready_for_transaction.set()

            self.transaction_ready.wait()
            print(f"Customer {self.id} [Teller {self.teller.id}]: asks for {self.transaction_type.lower()} transaction")

            self.transaction_done.wait()
            print(f"Customer {self.id} [Teller {self.teller.id}]: leaves teller")
            print(f"Customer {self.id} []: goes to door")
            print(f"Customer {self.id} []: leaves the bank")

    def selects_teller(self, teller):
        self.teller = teller
        self.transaction_ready = threading.Event()
        self.teller_ready.set()

    def give_transaction(self, teller):
        self.transaction_ready.set()
        return self.transaction_type

    def finish_interaction(self, teller):
        self.transaction_done.set()

if __name__ == "__main__":
    numCustomers = 50
    numTellers = 3

    entry = threading.Semaphore(2) #Semaphore to dictate entry 
    safe = threading.Semaphore(2) #Semaphore to dictate how many tellers can be inside the safe at once. 
    manager = threading.Semaphore(1) #Semaphore to dictate entry to see the manager. Only one teller at a time
    teller_ready_barrier = threading.Barrier(numTellers)  #Makes sure that the teller threads wait until all of them are ready
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

    print("The bank closes for the day")
