#!/bin/bash
#SBATCH --nodes=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=5G
#SBATCH --time=02:00:00
#SBATCH --mail-type=ALL
#SBATCH --mail-user=YOUR_EMAIL_ADDRESS
#SBATCH --job-name=Mastersfilt
#SBATCH --output=Masterfilt_%j.o
#SBATCH --error=Masterfilt_%j.e
#SBATCH --array=YOUR_ARRAY_SIZE

module load python scipy-stack
source $HOME/ENV2/bin/activate

filenames=($(cat /home/wendyy/projects/def-sushant/wendyy/mutshape/data/csv/skcm/skcm_csvs.txt))
csvfile=${filenames[${SLURM_ARRAY_TASK_ID}]}

python /home/wendyy/projects/def-sushant/wendyy/mutshape/scripts/snp_filter.py \
${csvfile}
