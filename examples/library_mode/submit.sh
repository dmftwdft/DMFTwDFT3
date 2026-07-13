#!/bin/bash
#SBATCH -J DMFTwDFT_run             # Job name
#SBATCH -p interactive         # Queue (partition) name
#SBATCH -N 1                 # Total # of nodes
#SBATCH --ntasks-per-node 16 # Tasks per node
#SBATCH --mem=100G           # Memory per node
#SBATCH -t 04:00:00

# Initialization
set -eo pipefail

source ~/.bashrc
ulimit -s unlimited
mamba activate dmft # Activate conda environment for DMFT
intel # Load Intel compiler

cd $SLURM_SUBMIT_DIR
mpirun -n $SLURM_NTASKS ./test.x > out 2> err
