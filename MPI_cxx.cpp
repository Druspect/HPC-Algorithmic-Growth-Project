#include <mpi.h>
#include <vector>
#include <algorithm>
#include <iostream>
#include <cstdlib>
#include <ctime>
#include <chrono>

using namespace std;

void bubble_sort(vector<int>& arr) {
    int n = arr.size();
    for (int i = 0; i < n-1; i++)    
        for (int j = 0; j < n-i-1; j++)
            if (arr[j] > arr[j+1])
                swap(arr[j], arr[j+1]);
}

void merge(vector<int>& left, vector<int>& right, vector<int>& bars) {
    int nL = left.size();
    int nR = right.size();
    int i = 0, j = 0, k = 0;

    while (j < nL && k < nR) {
        if (left[j] < right[k]) {
            bars[i] = left[j];
            j++;
        } else {
            bars[i] = right[k];
            k++;
        }
        i++;
    }
    while (j < nL) {
        bars[i] = left[j];
        j++; i++;
    }
    while (k < nR) {
        bars[i] = right[k];
        k++; i++;
    }
}

void merge_sort(vector<int>& arr) {
    if (arr.size() <= 1) return;

    int mid = arr.size() / 2;
    vector<int> left(arr.begin(), arr.begin()+mid);
    vector<int> right(arr.begin()+mid, arr.end());

    merge_sort(left);
    merge_sort(right);
    merge(left, right, arr);
}

void selection_sort(vector<int>& arr) {
    int n = arr.size();
    int minIdx;

    for (int i = 0; i < n-1; i++) {
        minIdx = i;
        for (int j = i+1; j < n; j++)
            if (arr[j] < arr[minIdx])
                minIdx = j;
        swap(arr[minIdx], arr[i]);
    }
}

int partition(vector<int>& arr, int low, int high) {
    int pivot = arr[high];
    int i = (low - 1);

    for (int j = low; j <= high- 1; j++) {
        if (arr[j] < pivot) {
            i++;
            swap(arr[i], arr[j]);
        }
    }
    swap(arr[i + 1], arr[high]);
    return (i + 1);
}

void quick_sort(vector<int>& arr, int low, int high) {
    if (low < high) {
        int pi = partition(arr, low, high);

        quick_sort(arr, low, pi - 1);
        quick_sort(arr, pi + 1, high);
    }
}

int main(int argc, char* argv[]) {
    MPI_Init(&argc, &argv);

    int world_rank;
    MPI_Comm_rank(MPI_COMM_WORLD, &world_rank);

    srand(time(NULL) + world_rank);

    vector<int> array_sizes = {500, 1000, 2000, 5000, 10000, 20000, 50000};

    vector<pair<string, void(*)(vector<int>&, int, int)>> sort_algorithms = {
        {"Bubble Sort", [](vector<int>& arr, int, int) { bubble_sort(arr); }},
        {"Merge Sort", [](vector<int>& arr, int, int) { merge_sort(arr); }},
        {"Selection Sort", [](vector<int>& arr, int, int) { selection_sort(arr); }},
        {"Quick Sort", quick_sort}
    };

    for (int size : array_sizes) {
        vector<int> data(size);

        for (int& val : data) {
            val = rand() % 10000;
        }

        for (auto& [name, sort_function] : sort_algorithms) {
            vector<int> arr = data; // Copy the original data for each sort

            auto start_time = chrono::high_resolution_clock::now();
            sort_function(arr, 0, arr.size() - 1);
            auto end_time = chrono::high_resolution_clock::now();
            auto duration = chrono::duration_cast<chrono::microseconds>(end_time - start_time).count();

            cout << "Process " << world_rank << " sorted array of size " << size << " using " << name << " in " << duration << " microseconds." << endl;
        }
    }

    MPI_Finalize();
    return 0;
}
