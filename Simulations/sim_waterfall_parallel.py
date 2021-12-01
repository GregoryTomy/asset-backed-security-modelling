"""This script contains code to parallelize the simulate waterfall function"""
from Simulations.sim_waterfall import simulate_waterfall
import multiprocessing
import numpy as np


def do_work(input, output):
    """Generic function that takes an input function and argument and runs it"""
    while True:
        try:
            f, args = input.get(timeout=1)
            results = f(*args)
            output.put(results)
        except:
            break


def simulate_waterfall_parallel(loanpool, structuredsecurity, num_sim, num_processes):
    """Runs waterfall in parallel processes"""
    input_queue = multiprocessing.Queue()
    output_queue = multiprocessing.Queue()
    sub_sims = int(num_sim / num_processes)

    for i in range(num_processes):
        input_queue.put((simulate_waterfall, (loanpool, structuredsecurity, sub_sims)))

    processes = []
    for i in range(num_processes):
        p = multiprocessing.Process(target=do_work, args=(input_queue, output_queue))
        processes.append(p)
        p.start()

    results = []

    while len(results) != num_processes:
        r = output_queue.get()
        r = np.array(r)
        results.append(r)

    for p in processes:
        p.terminate()

    res_sum = 0
    for i in range(len(results)):
        res_sum += results[i]

    res_average = res_sum / num_processes

    return [res_average[0], res_average[1], res_average[2]]  # match output to sim waterfall to keep the code the same
