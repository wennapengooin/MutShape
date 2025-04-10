#!/bin/bash
#SBATCH --nodes=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=10G
#SBATCH --time=00:30:00
#SBATCH --mail-type=ALL
#SBATCH --mail-user=wendy.wan@mail.utoronto.ca
#SBATCH --job-name=addcollapse
#SBATCH --output=/home/wendyy/scratch/oande/addcollapse.o
#SBATCH --error=/home/wendyy/scratch/oande/addcollapse.e

module load python scipy-stack
source $HOME/ENV2/bin/activate

python /home/wendyy/projects/def-sushant/wendyy/mutshape/scripts/collapse_sigs.py\
/home/wendyy/scratch/nodup_coad.csv
