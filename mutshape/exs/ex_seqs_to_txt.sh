#!/bin/bash
#SBATCH --nodes=1
#SBATCH --mem=5G
#SBATCH --time=00:30:00
#SBATCH --mail-type=ALL
#SBATCH --mail-user=YOUR_EMAIL_ADDRESS
#SBATCH --job-name=Masterseqstxt
#SBATCH --output=Masterseqstotxt_%j.o
#SBATCH --error=Masterseqstotxt_%j.e
#SBATCH --array=YOUR_ARRAY_SIZE

module load python scipy-stack
source $HOME/ENV2/bin/activate

csvnames=($(cat /home/wendyy/projects/def-sushant/wendyy/mutshape/data/csv/luad/luad_csvs.txt))
csvfile=${csvnames[${SLURM_ARRAY_TASK_ID}]}

python /home/wendyy/projects/def-sushant/wendyy/mutshape/scripts/seqs_to_txt.py \
${csvfile} /home/wendyy/scratch/luad/refseqs ref

python /home/wendyy/projects/def-sushant/wendyy/mutshape/scripts/seqs_to_txt.py \
${csvfile} /home/wendyy/scratch/luad/mutseqs mut
