import multiprocessing as mp
import random
import time

NUM_NUMBERS = 1000000
NUM_PROCESSES = 4

# (a) Versi Message Passing (Queue)
def worker_queue(q):
    numbers = [random.random() for _ in range(NUM_NUMBERS)]
    local_sum = sum(numbers)
    q.put(local_sum)

def run_queue_version():
    q = mp.Queue()
    processes = []
    
    start_time = time.time()
    for _ in range(NUM_PROCESSES):
        p = mp.Process(target=worker_queue, args=(q,))
        processes.append(p)
        p.start()
        
    total = sum(q.get() for _ in range(NUM_PROCESSES))
    for p in processes:
        p.join()
        
    elapsed = time.time() - start_time
    return total, elapsed

# (b) Versi Shared Memory (Value dengan Lock)
def worker_value(shared_val, lock):
    numbers = [random.random() for _ in range(NUM_NUMBERS)]
    local_sum = sum(numbers)
    
    # Mengunci hanya saat memperbarui nilai bersama
    with lock:
        shared_val.value += local_sum

def run_value_version():
    shared_val = mp.Value('d', 0.0)
    lock = mp.Lock()
    processes = []
    
    start_time = time.time()
    for _ in range(NUM_PROCESSES):
        p = mp.Process(target=worker_value, args=(shared_val, lock))
        processes.append(p)
        p.start()
        
    for p in processes:
        p.join()
        
    elapsed = time.time() - start_time
    return shared_val.value, elapsed

if __name__ == '__main__':
    tot_q, time_q = run_queue_version()
    print(f"[Queue / Message Passing] Total: {tot_q:.2f} | Waktu: {time_q:.4f} detik")

    tot_v, time_v = run_value_version()
    print(f"[Value / Shared Memory ] Total: {tot_v:.2f} | Waktu: {time_v:.4f} detik")