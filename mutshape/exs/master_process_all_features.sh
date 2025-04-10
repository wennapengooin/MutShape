#!/bin/bash
#SBATCH --nodes=2
#SBATCH --cpus-per-task=2
#SBATCH --mem=8G
#SBATCH --time=04:00:00
#SBATCH --mail-type=ALL
#SBATCH --mail-user=YOUR_EMAIL_ADDRESS
#SBATCH --job-name=MasterProcessAll
#SBATCH --output=MasterProcessAll_%j.o
#SBATCH --error=MasterProcessAll_%j.e
#SBATCH --array=YOUR_ARRAY_SIZE

module load python scipy-stack
source $HOME/ENV2/bin/activate

# Define input files
csvnames=($(cat /home/wendyy/projects/def-sushant/wendyy/mutshape/data/csv/skcm/skcm_csvs.txt))
csvfile=${csvnames[${SLURM_ARRAY_TASK_ID}]}

mutnames=($(cat /home/wendyy/scratch/skcm/MGW/mutshape.txt))
mutfile=${mutnames[${SLURM_ARRAY_TASK_ID}]}

refnames=($(cat /home/wendyy/scratch/skcm/MGW/refshape.txt))
reffile=${refnames[${SLURM_ARRAY_TASK_ID}]}

# Run the combined processing script
python /home/wendyy/projects/def-sushant/wendyy/mutshape/scripts/process_all_features.py \
${csvfile} ${mutfile} ${reffile}