#!/bin/bash
#SBATCH --nodes=2
#SBATCH --cpus-per-task=2
#SBATCH --mem=50G
#SBATCH --time=09:00:00
#SBATCH --mail-type=ALL
#SBATCH --mail-user=YOUR_EMAIL_ADDRESS
#SBATCH --job-name=MasterGetDNAshape
#SBATCH --output=MasterGetDNAshape_%j.o
#SBATCH --error=MasterGetDNAshape_%j.e
#SBATCH --array=YOUR_ARRAY_SIZE

module load python/3.10.13
source $HOME/ENV/bin/activate

# Get mutant sequences
names=($(cat /home/wendyy/scratch/skcm/mutseqs_skcm.txt))
files=${names[${SLURM_ARRAY_TASK_ID}]}

python /home/wendyy/projects/def-sushant/wendyy/mutshape/scripts/get_dna_shape.py \
${files} /home/wendyy/scratch/skcm/Stagger/mutshape Stagger 

python /home/wendyy/projects/def-sushant/wendyy/mutshape/scripts/get_dna_shape.py \
${files} /home/wendyy/scratch/skcm/Buckle/mutshape Buckle

python /home/wendyy/projects/def-sushant/wendyy/mutshape/scripts/get_dna_shape.py \
${files} /home/wendyy/scratch/skcm/Opening/mutshape Opening

python /home/wendyy/projects/def-sushant/wendyy/mutshape/scripts/get_dna_shape.py \
${files} /home/wendyy/scratch/skcm/Shift/mutshape Shift

python /home/wendyy/projects/def-sushant/wendyy/mutshape/scripts/get_dna_shape.py \
${files} /home/wendyy/scratch/skcm/Slide/mutshape Slide

python /home/wendyy/projects/def-sushant/wendyy/mutshape/scripts/get_dna_shape.py \
${files} /home/wendyy/scratch/skcm/Tilt/mutshape Tilt

python /home/wendyy/projects/def-sushant/wendyy/mutshape/scripts/get_dna_shape.py \
${files} /home/wendyy/scratch/skcm/Roll/mutshape Roll

python /home/wendyy/projects/def-sushant/wendyy/mutshape/scripts/get_dna_shape.py \
${files} /home/wendyy/scratch/skcm/HelT/mutshape HelT
