#!/bin/bash
#SBATCH --nodes=1
#SBATCH --mem=2G
#SBATCH --time=00:05:00
#SBATCH --mail-type=ALL
#SBATCH --YOUR EMAIL ADDRESS
#SBATCH --job-name=dl_ref_genome
#SBATCH --output=dl_ref_genome.o
#SBATCH --error=dl_ref_genome.e

source $HOME/ENV/bin/activate
module load python

# Define Compute Canada username
USER=your_username

# Replace variables if needed
URL="https://hgdownload.soe.ucsc.edu/goldenPath/hg38/bigZips/hg38.fa.gz"
DOWNLOAD_PATH="/home/${USER}/projects/def-sushant/${USER}/mutshape/data/reffasta"
LOG_FILE="/home/${USER}/projects/def-sushant/${USER}/mutshape/data/reffasta/download_log.txt"

# Run the Python script with arguments
python /home/${USER}/projects/def-sushant/${USER}/mutshape/scripts/dl_ref_genome.py $URL $DOWNLOAD_PATH $LOG_FILE

# Unzip the downloaded file
gunzip ${DOWNLOAD_PATH}/hg38.fa.gz