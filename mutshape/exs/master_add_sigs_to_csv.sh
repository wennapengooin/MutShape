#!/bin/bash
#SBATCH --nodes=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=3G
#SBATCH --time=00:45:00
#SBATCH --mail-type=ALL
#SBATCH --mail-user=YOUR_EMAIL_ADDRESS
#SBATCH --job-name=Masterdecompsigs
#SBATCH --output=Masterdecompsigs_%j.o
#SBATCH --error=Masterdecompsigs_%j.e
#SBATCH --array=YOUR_ARRAY_SIZE

module load python scipy-stack
source $HOME/ENV2/bin/activate

decompsignames=($(cat /home/wendyy/projects/def-sushant/wendyy/mutshape/data/maf/skcm/skcm_decomposed_sigs.txt))
decompsigfile=${decompsignames[${SLURM_ARRAY_TASK_ID}]}

python /home/wendyy/projects/def-sushant/wendyy/mutshape/scripts/add_decomposed_sigs.py \
${decompsigfile} /home/wendyy/projects/def-sushant/wendyy/mutshape/data/csv/skcm
