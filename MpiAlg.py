#!/usr/bin/env python3
from mpi4py import MPI
import random
import time

# Initialize MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# Define sorting algorithms
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

def merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2
        L = arr[:mid]
        R = arr[mid:]

        merge_sort(L)
        merge_sort(R)

        i = j = k = 0

        while i < len(L) and j < len(R):
            if L[i] < R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1

        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1

        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1
    return arr

def selection_sort(arr):
    for i in range(len(arr)):
        min_idx = i
        for j in range(i+1, len(arr)):
            if arr[min_idx] > arr[j]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr

def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    else:
        pivot = arr[0]
        less_than_pivot = [x for x in arr[1:] if x <= pivot]
        greater_than_pivot = [x for x in arr[1:] if x > pivot]
        return quick_sort(less_than_pivot) + [pivot] + quick_sort(greater_than_pivot)

# Define sorting algorithms and their names for easy iteration
sort_algorithms = {
    "Bubble Sort": bubble_sort,
    "Merge Sort": merge_sort,
    "Selection Sort": selection_sort,
    "Quick Sort": quick_sort
}

# Split array sizes across nodes (simplified example)
array_sizes = [500, 1000, 2000, 5000, 10000, 20000, 50000]
local_array_size = array_sizes[rank % len(array_sizes)]  # Simplified distribution

# Generate a random list of integers for the assigned array size
arr = [random.randint(0, 10000) for _ in range(local_array_size)]

# Execute sorting algorithms on the assigned array size
results = {}
for name, algorithm in sort_algorithms.items():
    start_time = time.time_ns()
    algorithm(arr.copy())  # Assuming the sorting function modifies the array in place
    end_time = time.time_ns()
    dur_microseconds = (end_time - start_time) / 1000
    results[name] = dur_microseconds

# Gather results at the master node
all_results = comm.gather(results, root=0)

# Master node aggregates and prints results
if rank == 0:
    # Aggregate and print results (to be implemented)
    pass
