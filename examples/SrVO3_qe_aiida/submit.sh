#!/bin/bash
#SBATCH -J DMFTwDFT_run             # Job name
#SBATCH -p interactive         # Queue (partition) name
#SBATCH -N 4                 # Total # of nodes
#SBATCH --ntasks-per-node 64 # Tasks per node
#SBATCH --mem=100G           # Memory per node
#SBATCH -t 04:00:00

# Initialization
set -eo pipefail

source ~/.bashrc
ulimit -s unlimited
mamba activate dmft # Activate conda environment for DMFT
intel # Load Intel compiler

cd $SLURM_SUBMIT_DIR
echo "mpirun -n $SLURM_NTASKS" > para_com.dat
DMFT.py -dmft -v -dft qe -aiida 2>&1 | tee dmft.log
cd DMFT
postDMFT.py ac -siglistindx 4 2>&1 | tee ac.log
postDMFT.py dos 2>&1 | tee dos.log
postDMFT.py bands -plotplain -rom 1000 -kpband 1000 -normalize 2>&1 | tee bands.log
