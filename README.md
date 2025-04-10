# MutShape: A Mutational Signature and DNA Shape Analysis Pipeline
==============================================

This README outlines the complete pipeline for analyzing mutational signatures and DNA shape features in cancer samples. The pipeline consists of two main components:

1. **Mutational Signature Analysis** using SigProfilerAssignment
2. **DNA Shape Prediction** using deepDNAshape

## Table of Contents
-----------------

- [MutShape: A Mutational Signature and DNA Shape Analysis Pipeline](#mutshape-a-mutational-signature-and-dna-shape-analysis-pipeline)
  - [Table of Contents](#table-of-contents)
  - [Directory Structure](#directory-structure)
  - [Environment Setup](#environment-setup)
    - [For SigProfilerAssignment:](#for-sigprofilerassignment)
    - [For deepDNAshape:](#for-deepdnashape)
    - [General Instructions for SLURM Scripts](#general-instructions-for-slurm-scripts)
  - [Data Acquisition](#data-acquisition)
    - [Download MAF and CSV files locally:](#download-maf-and-csv-files-locally)
    - [Download reference FASTA](#download-reference-fasta)
  - [Mutational Signature Analysis](#mutational-signature-analysis)
  - [DNA Shape Prediction](#dna-shape-prediction)
  - [Data Processing and Visualization](#data-processing-and-visualization)
    - [Links to Specific Sections:](#links-to-specific-sections)

## Directory Structure

```
mutshape/
│
├── data/
│   ├── maf/
│   ├── csv/
│   └── reffasta/
│
├── tools/
│
├── scripts/
│
└── exs/
```

This structure shows the main `mutshape` directory containing:
- `data/`: For storing various data files
  - `maf/`: MAF files
  - `csv/`: CSV files
  - `reffasta/`: Reference FASTA files
- `tools/`: For storing tools and software
- `scripts/`: For storing scripts
- `exs/`: For storing execution scripts

## Environment Setup
-------------------
SigProfilerAssignment and deepDNAshape require different environments to run correctly.

### For SigProfilerAssignment:
Load the required modules:
1. python
2. scipy-stack
   
Create an environment with the following dependencies:
1. SigProfilerAssignment

```bash
module load StdEnv/2023 python scipy-stack      # load python and scipy-stack
virtualenv --no-download ENV2                   # create an environment (in this case named ENV2)
source ENV2/bin/activate                        # activate the environment
pip install --no-index --upgrade pip            # upgrade pip to the latest version
pip install SigProfilerAssignment               # in the tools directory, install SigProfilerAssignment (it will be in your environment the next time you activate it)

```

### For deepDNAshape:
Load the required modules:
1. python 3.10.13
2. scipy-stack
   
Create an environment (with a different name) with the following dependencies:
1. numpy ver. 1.23.5
2. tensorflow ver. 2.15.1
3. pyfaidx
4. deepDNAshape

```bash
module load StdEnv/2023 python/3.10.13               # load python and scipy-stack
virtualenv --no-download ENV                         # create an environment (in this case named ENV)
source ENV/bin/activate                              # activate the environment
pip install --no-index --upgrade pip                 # upgrade pip to the latest version
PYTHONPATH="" pip install numpy==1.23.5              # install older version to override version from scipy-stack
pip install tensorflow==2.15.1                       # install tensorflow ver. 2.15.1 
pip install pyfaidx                                  # install pyfaidx
git clone https://github.com/JinsenLi/deepDNAshape   # in the tools directory, clone deepDNAshape repository
cd deepDNAshape                                      # enter deepDNAshape repository
pip install .                                        # install deepDNAshape
```

### General Instructions for SLURM Scripts

Before running any SLURM script (`sbatch`), ensure the following:

1. **Input Filenames**:
   - Update the variables in the script (e.g., `csvnames`, `mutnames`, `refnames`, `seqnames`) to point to the correct text files containing the list of input files.

2. **Array Size**:
   - Adjust the `--array` parameter in the SLURM script to match the number of input files listed in the corresponding text file.

3. **Email Notifications**:
   - Replace `YOUR_EMAIL_ADDRESS` in the `--mail-user` parameter with your email address to receive job notifications.

4. **File Paths**:
   - Verify and update all file paths in the script to match your directory structure.

5. **Reference Files**:
   - Ensure the reference FASTA file and other required files are correctly specified in the script.


## Data Acquisition
------------------

### Download MAF and CSV files locally:

Use the R script to download MAF and CSV files of a cancer project from TCGA to your local machine. An example done for TCGA-SKCM is provided below:

*Note: the CSV files are downloaded and renamed to its corresponding TCGA Barcode for streamlined data processing. For more information on what a TCGA Barcode is [click here](https://docs.gdc.cancer.gov/Encyclopedia/pages/TCGA_Barcode/)*

```r
setwd("path_to_local_maf_directory") # specify the directory you want the files to be stored in

library(TCGAbiolinks) # To query MAF files
library(maftools) # To convert MAF into CSV files

query <- GDCquery( # Query cancer project MAF files
  project = "TCGA-SKCM", 
  data.category = "Simple Nucleotide Variation",
  data.type = "Masked Somatic Mutation",
  access = "open"
)
GDCdownload(query) # Download queried MAF files

results <- query[[1]][[1]]

all_barcodes <- character() # make vector storing barcode names
for (row in 1:nrow(results)) {
  all_barcodes <- results[row, 'cases']
  parsed_barcodes <- strsplit(barcodes, ",")[[1]]
  tumor_barcode <- parsed_barcodes[1]
  barcodes <- c(all_barcodes, tumor_barcode)
}

for (i in 1:length(barcodes)) { # Loop over vector of barcode names and save files to CSV
  indv_barcode = barcodes[i]
  lst_barcode = c(indv_barcode)
  indv_coad <- GDCquery(
    project = "TCGA-SKCM", 
    data.category = "Simple Nucleotide Variation",
    data.type = "Masked Somatic Mutation",
    access = "open",
    barcode = lst_barcode
  )
  path = "path_to_local_csv_directory"
  csv_name = paste(path, indv_barcode,".csv")
  maf <- GDCprepare(inv_coad)
  write.csv(maf, csv_name, row.names = FALSE)
}
```
Following the downloads, move the MAF and/or CSV files from local to virtual using the command `scp -r`.

### Download reference FASTA

```bash
   sbatch ex_dl_ref_genome.sh
```
*Replace any defined variables if needed (url, file paths, etc.)*

## Mutational Signature Analysis
------------------------------

1. **Install Reference Genome**:
Install your desired reference genome as follows (available reference genomes are: GRCh37, GRCh38, mm9, mm10, and rn6):

   ```python
   from SigProfilerMatrixGenerator import install as genInstall
   genInstall.install('GRCh38')
   ```

2. **Prepare MAF Files**:
If you used `scp -r` to copy the MAF files from local to virtual, they will be compressed.

   *Note: ensure you have permissions to uncompress*

   ```bash
   gzip -dr /home/wendyy/scratch/maf/{cancer}/  # Uncompress directory containing maf.gz files
   ```

3. **Run SigProfilerAssignment**:
   1. Create a text file containing all the maf directories in the cancer project.
   2. Run the executable, remembering to change the array number to the number of MAF files
   3. **IMPORTANT**: Some MAF files may be empty. Reconfigure the text file containing all the MAF directories **AND** Reconfigure the text file containing all the CSV  directories.

   ```bash
   sbatch master_get_sigs.sh
   ```

4. **Map Signature to Mutation**
   Appends the signatures with the highest probabilities of each mutation to the CSV of the corresponding sample.

   ```bash
   sbatch master_add_decomposed_sigs.sh
   ```

## DNA Shape Prediction
----------------------

1. **Filter CSVs for SNPs**:
   ```bash
   sbatch ex_filter_for_snps.sh
   ```

2. **Add Flanking Sequences**:
   ```bash
   sbatch master_add_contexts.sh
   ```
3. **Transfer reference and mutant sequences to TXT files**
   1. Create folders in `scratch` to store TXTs containing mutant and reference. sequences: `mkdir ./{cancer}/mutseqs/` and `mkdir ./{cancer}/refseqs/`.
   2. Transfers sequences.
  ```bash
  sbatch ex_seqs_to_txt.sh
  ```
   3. Put all names of TXT files containing sequences into a new TXT file.
   eg. `ls /home/wendyy/scratch/coad/refseqs/* > /home/wendyy/scratch/coad/refseqs.txt` and `ls /home/wendyy/scratch/coad/mutseqs/* > /home/wendyy/scratch/coad/mutseqs.txt`
   
1. **Predict DNA shape**:
   1. Create folders to hold the DNA shape values of mutant and wildtype DNA shape features.
   eg. `mkdir ./{cancer}/{feature}/mutshape/` and `mkdir ./{cancer}/{feature}/refshape/`
   2. Run deepDNAshape. 
   
   ```bash
   sbatch master_get_dna_shape
   ```
   3.  Put all names of TXT files containing DNA shape values into a new TXT file.
   eg. `ls /home/wendyy/scratch/{cancer}/{feature}/mutshape/*.txt > /home/wendyy/scratch/{cancer}/{feature}/mutshape.txt` and `ls /home/wendyy/scratch/{cancer}/{feature}/refshape/*.txt > /home/wendyy/scratch/{cancer}/{feature}/refshape.txt`

## Data Processing and Visualization
-----------------------------------

**Calculate Euclideans, removing duplicates, adding mutation type**:
```bash
sbatch master_process_all_features.sh # Calculate and add Euclidean distance, sign, signed Euclidean distance, and sequence values
python no_dup.py <csv_file> # Remove duplicate mutations
```


For more detailed instructions on specific parts of the pipeline, please refer to the linked sections above.

### Links to Specific Sections:

- [MutShape: A Mutational Signature and DNA Shape Analysis Pipeline](#mutshape-a-mutational-signature-and-dna-shape-analysis-pipeline)
  - [Table of Contents](#table-of-contents)
  - [Directory Structure](#directory-structure)
  - [Environment Setup](#environment-setup)
    - [For SigProfilerAssignment:](#for-sigprofilerassignment)
    - [For deepDNAshape:](#for-deepdnashape)
    - [General Instructions for SLURM Scripts](#general-instructions-for-slurm-scripts)
  - [Data Acquisition](#data-acquisition)
    - [Download MAF and CSV files locally:](#download-maf-and-csv-files-locally)
    - [Download reference FASTA](#download-reference-fasta)
  - [Mutational Signature Analysis](#mutational-signature-analysis)
  - [DNA Shape Prediction](#dna-shape-prediction)
  - [Data Processing and Visualization](#data-processing-and-visualization)
    - [Links to Specific Sections:](#links-to-specific-sections)

---
