#!/bin/bash
#SBATCH -J VO2_monolayer     # Job name
#SBATCH -p interactive       # Queue (partition) name
#SBATCH -N 1                 # Total # of nodes
#SBATCH --ntasks-per-node 64 # Tasks per node
#SBATCH --mem=100G           # Memory per node
#SBATCH -t 08:00:00

# Initialization
set -eo pipefail

source ~/.bashrc
ulimit -s unlimited
mamba activate dmft # Activate conda environment for DMFT
intel # Load Intel compiler

cd $SLURM_SUBMIT_DIR
echo "mpirun -n $SLURM_NTASKS" > para_com.dat
DMFT.py dmft --verbose --dft vasp 2>&1 | tee dmft.log

cd DMFT
postDMFT.py ac --average 10 2>&1 | tee ac.log
postDMFT.py dos 2>&1 | tee dos.log

# The built-in default k-path is simple cubic and includes R = (1/2,1/2,1/2),
# which is meaningless for a slab. KPOINTS.band supplies Gamma-X-M-Gamma at
# kz = 0 instead. --kpoints points at it so that neither it nor the SCF KPOINTS
# has to be copied or renamed.
postDMFT.py bands --plot-plain --omega-points 1000 --band-k-points 1000 --normalize \
    --auto-k-path --kpoints ../KPOINTS.band 2>&1 | tee bands.log

# The same path without a file:
# postDMFT.py bands --plot-plain --omega-points 1000 --band-k-points 1000 --normalize \
#     --k-point-list 0 0 0 --k-point-list 0.5 0 0 --k-point-list 0.5 0.5 0 --k-point-list 0 0 0
