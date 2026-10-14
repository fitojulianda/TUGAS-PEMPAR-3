import multiprocessing as mp
import time
import math

# Fungsi CPU-bound untuk mengecek bilangan prima
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(math.isqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def hitung_prima(start_range, end_range):
    return sum(1 for i in range(start_range, end_range) if is_prime(i))

def worker_task(args):
    return hitung_prima(*args)

def get_chunks(limit, n_workers):
    chunk_size = limit // n_workers
    return [(i * chunk_size, (i + 1) * chunk_size) for i in range(n_workers)]

if __name__ == '__main__':
    # Diturunkan ke 500.000 agar eksekusi cepat namun karakteristik speedup tetap terlihat
    limit = 500000  
    worker_counts = [1, 2, 4, 8]
    execution_times = []

    # Penanganan konteks untuk Windows ('spawn')
    try:
        ctx = mp.get_context('fork')
    except ValueError:
        ctx = mp.get_context('spawn')

    print("Mulai menghitung...")
    for workers in worker_counts:
        chunks = get_chunks(limit, workers)
        start_time = time.time()
        
        with ctx.Pool(processes=workers) as pool:
            results = pool.map(worker_task, chunks)
            
        elapsed = time.time() - start_time
        execution_times.append(elapsed)
        print(f"Workers: {workers:2d} | Waktu Eksekusi: {elapsed:.4f} detik")

    # Menghitung Speedup
    t1 = execution_times[0]
    actual_speedup = [t1 / t for t in execution_times]
    
    # Teori Hukum Amdahl (p = 0.95)
    p = 0.95
    amdahl_speedup = [1 / ((1 - p) + (p / w)) for w in worker_counts]

    # Import matplotlib HANYA saat akan membuat plot (menghemat overhead spawn)
    import matplotlib.pyplot as plt

    plt.figure(figsize=(8, 5))
    plt.plot(worker_counts, actual_speedup, marker='o', label='Speedup Aktual', linewidth=2)
    plt.plot(worker_counts, amdahl_speedup, marker='s', linestyle='--', label='Hukum Amdahl (p=0.95)', linewidth=2)
    plt.plot(worker_counts, worker_counts, marker='^', linestyle=':', label='Speedup Ideal (Linier)', linewidth=1)
    
    plt.title("Analisis Speedup Skala vs Hukum Amdahl")
    plt.xlabel("Jumlah Worker")
    plt.ylabel("Speedup")
    plt.xticks(worker_counts)
    plt.legend()
    plt.grid(True)
    plt.show()