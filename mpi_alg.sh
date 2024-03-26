#!/bin/bash
#SBATCH --job-name=sort-test
#SBATCH --nodes=7
#SBATCH --ntasks-per-node=32
#SBATCH --time=05:00:00
#SBATCH --output=sort-test-%j.out

module load gcc/11.2.0 python39 python3 openmpi4/gcc/4.1.5

mpirun /home/fuller_m@utpb.edu/scripts/MpiAlg.py

