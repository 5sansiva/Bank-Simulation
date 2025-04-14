# Multithreaded Bank Simulation

This project is a **multithreaded simulation** of a bank with **3 tellers** and **50 customers**, written in **Python** using the `threading` module. It demonstrates concepts of **concurrency**, **synchronization**, and **inter-thread communication** through a realistic simulation involving shared resources such as a bank manager and a safe.

The simulation models the workflow of customers entering the bank, waiting in line, and being served by tellers who interact with the manager and perform transactions in a safe with limited access.

## Overview

The simulation consists of:

- **Customer Threads:** Represent customers who want to perform either a deposit or withdrawal transaction.
- **Teller Threads:** Represent bank tellers who serve customers, process transactions, consult the manager, and access the safe when necessary.
- **Manager Access:** Only one teller can consult the manager at any given time.
- **Safe Access:** Only two tellers can be inside the safe at the same time.
- **Entry Control:** Only two customers may enter the bank at once.
- **Teller Synchronization:** All tellers must be ready before the bank begins processing customers.

The system uses a **shared queue** where customers are queued and assigned to available tellers. Once all customers have been served, tellers shut down gracefully, and the bank closes for the day.

## Components

### Tellers

- Spawned at the beginning of the simulation.
- Wait until all other tellers are ready using a `threading.Barrier`.
- Retrieve customers from a shared `Queue`.
- For **withdrawal** transactions:
  - Request permission from the manager using a binary semaphore (`manager`).
  - Access the safe using a semaphore (`safe`) allowing up to two tellers at once.
- For **deposit** transactions:
  - Directly access the safe.
- After completing a transaction, the teller waits for the next customer.

### Customers

- Each customer is assigned a transaction type (randomly selected as either `deposit` or `withdrawal`).
- Controlled entry using a semaphore (`entry`) allowing only two customers to enter the bank simultaneously.
- Once inside, customers enqueue themselves into the shared `Queue` to wait for an available teller.
- After the transaction, the customer exits the bank.

### Manager and Safe

- The manager is modeled with a binary semaphore (`manager`) that ensures only one teller interacts with the manager at a time.
- The safe is modeled with a semaphore (`safe`) allowing two tellers simultaneous access.

## Program Flow

1. Initialize semaphores and shared queue.
2. Spawn and start teller threads.
3. Spawn and start customer threads.
4. Customers enter the bank (limited to 2 at a time), select a teller, and perform their transaction.
5. Once all customers have been processed, `None` values are pushed into the queue to signal tellers to exit.
6. All threads join back, and the simulation ends with a shutdown message.

## How to Run

Make sure to have python3 installed on the system.
Check the version of python on your system by performing either python --version or python3 --verion. The version should be above Python 3.10 or higher.

To test on the UTD cs1 servers, run the project with this command: python3 bankSimulation.py

This will print out the desired output and have no major errors associated.
