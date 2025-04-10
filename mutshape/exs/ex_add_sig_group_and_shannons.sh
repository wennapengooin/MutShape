#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks=2
#SBATCH --cpus-per-task=2
#SBATCH --mem=1G
#SBATCH --time=00:03:00
#SBATCH --mail-type=ALL
#SBATCH --mail-user=wendy.wan@mail.utoronto.ca
#SBATCH --job-name=shannon
#SBATCH --output=shannon.o
#SBATCH --error=shannon.e

module load python scipy-stack
source $HOME/ENV2/bin/activate

python /home/wendyy/projects/def-sushant/wendyy/mutshape/scripts/collapse_sigs.py \
/home/wendyy/projects/def-sushant/wendyy/mutshape/data/merged_maf/skcm.csv

python /home/wendyy/projects/def-sushant/wendyy/mutshape/visualize/mutsigs/add_shannon.py \
/home/wendyy/projects/def-sushant/wendyy/mutshape/data/mutsigs/collapsed_skcm.csv



