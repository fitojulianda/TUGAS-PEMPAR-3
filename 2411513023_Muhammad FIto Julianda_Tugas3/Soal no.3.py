import multiprocessing as mp
import time
import math

def is_prime(n):
    if n < 2: return False
    for i in range(2, int(math.isqrt(n)) + 1):
        if n % i == 0: return False
    return True

def producer(task_queue, num_tasks):
    # Mengirim rentang angka sebagai tugas komputasi CPU-bound
    for i in range(num_tasks):
        task_queue.put(i * 50000)
    
    # Sinyal penghentian (poison pill)
    task_queue.put(None)

def consumer(task_queue, result_queue):
    while True:
        start_num = task_queue.get()
        if start_num is None:
            # Diteruskan ke consumer lain jika ada, lalu berhenti
            task_queue.put(None)
            break
        
        # Tugas CPU-bound: Menghitung bilangan prima
        count = sum(1 for i in range(start_num, start_num + 50000) if is_prime(i))
        result_queue.put((start_num, count))

if __name__ == '__main__':
    task_queue = mp.Queue()
    result_queue = mp.Queue()
    
    prod = mp.Process(target=producer, args=(task_queue, 10))
    cons1 = mp.Process(target=consumer, args=(task_queue, result_queue))
    cons2 = mp.Process(target=consumer, args=(task_queue, result_queue))
    
    start_time = time.time()
    prod.start()
    cons1.start()
    cons2.start()
    
    prod.join()
    cons1.join()
    cons2.join()
    
    elapsed = time.time() - start_time
    print(f"Producer-Consumer (Multiprocessing) selesai dalam {elapsed:.4f} detik.")