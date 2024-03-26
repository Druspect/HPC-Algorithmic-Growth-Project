import random
import time

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

array_sizes = [500, 1000, 2000, 5000, 10000, 20000, 50000]
# Generate a random list of integers
for size in array_sizes:
    print(f"\nArray Size: {size}")
    arr = [random.randint(0, 10000) for _ in range(size)]
    
# Time and run each sorting algorithm
    for name, algorithm in sort_algorithms.items():
        start_time = time.time_ns()
        sorted_arr = algorithm(arr.copy())
        end_time = time.time_ns()
        dur_microseconds = (end_time - start_time) / 1000
        print(f"{name} took {dur_microseconds} microseconds.")
