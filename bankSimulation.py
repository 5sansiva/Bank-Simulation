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
        self.busy = threading.Event()

    def run(self):
        print(f"Teller {self.id} []: ready to serve")
        print(f"Teller {self.id} []: waiting for a customer")

        teller_ready_barrier.wait()

        while True:
            customer = self.customerQueue.get()
            if customer is None:
                print(f"Teller {self.id} []: leaving for the day")
                break

            self.busy.set()  # Mark teller as busy
            
            # Notify customer about assigned teller
            customer.set_teller(self)
            
            # Wait for customer to complete their introduction
            customer.introduction_complete.wait()

            # Now proceed with serving the customer
            print(f"Teller {self.id} [Customer {customer.id}]: serving a customer")
            print(f"Teller {self.id} [Customer {customer.id}]: asks for transaction")
            
            # Wait for customer to be ready to give transaction
            customer.transaction_ready.wait()
            transaction_type = customer.transaction_type

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
            customer.transaction_complete.set()
            customer.customer_left.wait()
            
            self.busy.clear()  # Mark teller as not busy
            print(f"Teller {self.id} []: waiting for a customer")

class Customer(threading.Thread):
    def __init__(self, id, entry_semaphore, teller_queue):
        super().__init__()
        self.id = id
        self.entry_semaphore = entry_semaphore
        self.teller_queue = teller_queue
        self.transaction_type = random.choice(["Deposit", "Withdrawal"])
        self.teller = None
        self.teller_assigned = threading.Event()
        self.introduction_complete = threading.Event()
        self.transaction_ready = threading.Event()
        self.transaction_complete = threading.Event()
        self.customer_left = threading.Event()

    def run(self):
        print(f"Customer {self.id} []: wants to perform a {self.transaction_type.lower()} transaction")
        time.sleep(random.uniform(0, 0.1))

        print(f"Customer {self.id} []: going to bank.")
        with self.entry_semaphore:
            print(f"Customer {self.id} []: entering bank.")
            print(f"Customer {self.id} []: getting in line.")

            # Put customer in queue and wait to be assigned a teller
            self.teller_queue.put(self)
            self.teller_assigned.wait()

            # Now the customer has been assigned a teller
            print(f"Customer {self.id} []: selecting a teller.")
            print(f"Customer {self.id} [Teller {self.teller.id}]: selects teller")
            print(f"Customer {self.id} [Teller {self.teller.id}]: introduces itself")
            
            # Signal that introduction is complete
            self.introduction_complete.set()
            
            # Signal ready to give transaction
            self.transaction_ready.set()
            
            # Wait for transaction to complete
            self.transaction_complete.wait()
            
            print(f"Customer {self.id} [Teller {self.teller.id}]: leaves teller")
            print(f"Customer {self.id} []: goes to door")
            print(f"Customer {self.id} []: leaves the bank")
            
            # Signal that customer has left
            self.customer_left.set()

    def set_teller(self, teller):
        self.teller = teller
        self.teller_assigned.set()

if __name__ == "__main__":
    numCustomers = 50
    numTellers = 3

    entry = threading.Semaphore(2)  # Only 2 customers can enter at once
    safe = threading.Semaphore(2)   # Safe can handle 2 tellers at once
    manager = threading.Semaphore(1)  # Only 1 teller can talk to manager at once
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

    print("The bank closes for the day")