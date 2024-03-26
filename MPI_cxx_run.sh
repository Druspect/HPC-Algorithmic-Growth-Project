#!/bin/bash
#SBATCH --job-name=mpi_sort_test
#SBATCH --nodes=7
#SBATCH --ntasks-per-node=32
#SBATCH --time=00:10:00
#SBATCH --output=mpi_sort_test_%j.out

module load gcc/11.2.0 openmpi4/gcc/4.1.5

# Compile the MPI program
mpicxx -o MpiAlg_cxx /home/fuller_m@utpb.edu/scripts/MPI_cxx.cpp

# Run the MPI program
mpirun ./MpiAlg_cxx
