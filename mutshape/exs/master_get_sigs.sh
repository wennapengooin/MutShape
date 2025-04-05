#!/bin/bash
#SBATCH --nodes=2
#SBATCH --cpus-per-task=2
#SBATCH --mem=20G
#SBATCH --time=03:00:00
#SBATCH --mail-type=ALL
#SBATCH --mail-user=wendy.wan@mail.utoronto.ca
#SBATCH --job-name=Mastersigs
#SBATCH --output=Mastersigs_%j.o
#SBATCH --error=Mastersigs_%j.e
#SBATCH --array=0-ADJUST_ARRAY_SIZE

module load python scipy-stack
source $HOME/ENV2/bin/activate

names=($(cat /home/wendyy/scratch/maf/gbm/gbm_mafs.txt))
maf_dir=${names[${SLURM_ARRAY_TASK_ID}]}

python /home/wendyy/projects/def-sushant/wendyy/mutshape/scripts/get_sigs.py \
${maf_dir} ${maf_dir}
