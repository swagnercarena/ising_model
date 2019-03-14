#!/bin/bash
#
#SBATCH --partition=iric,hns,normal
#SBATCH --ntasks=1 #Number of CPUS
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=1GB
#SBATCH --time=0-01:00:00  # time (HH:MM:SS)
#SBATCH -o /home/users/swagnerc/phys_212/slurm_output/sampling.%N.%j.out # STDOUT
#SBATCH -e /home/users/swagnerc/phys_212/slurm_output/sampling.%N.%j.err # STDERR

python param_search.py ${1} ${2} ${3} ${4}
