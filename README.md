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

Replace any defined variables (url, file paths, etc.) if needed

```bash
   sbatch dl_ref_genome.sh
```

## Mutational Signature Analysis
------------------------------

1. **Install Reference Genome**:
Install your desired reference genome as follows (available reference genomes are: GRCh37, GRCh38, mm9, mm10, and rn6):

   ```python
   from SigProfilerMatrixGenerator import install as genInstall
   genInstall.install('GRCh38')
   ```

1. **Prepare MAF Files**:
If you used `scp -r` to copy the MAF files from local to virtual, they will be compressed.

   ```bash
   gzip -dr /home/wendyy/scratch/maf/{cancer}  # uncompress directory containing maf.gz files
   ```

1. **Run SigProfilerAssignment**:
   ```bash
   sbatch master_get_sig.sh
   ```

## DNA Shape Prediction
----------------------

1. **Filter CSVs for SNPs**:
   ```bash
   sbatch ex_snp_filter.sh
   ```

2. **Add Flanking Sequences**:
   ```bash
   sbatch master_addflanktnc.sh
   ```

3. **Run deepDNAshape**:
   ```bash
   sbatch master_calcadd.sh
   ```

## Data Processing and Visualization
-----------------------------------

**Specifying siggroups, removing duplicates, adding mutation type**:
```bash
# TBD
```


For more detailed instructions on specific parts of the pipeline, please refer to the linked sections above.

### Links to Specific Sections:

- [MutShape: A Mutational Signature and DNA Shape Analysis Pipeline](#mutshape-a-mutational-signature-and-dna-shape-analysis-pipeline)
  - [Table of Contents](#table-of-contents)
  - [Directory Structure](#directory-structure)
  - [Environment Setup](#environment-setup)
    - [For SigProfilerAssignment:](#for-sigprofilerassignment)
    - [For deepDNAshape:](#for-deepdnashape)
  - [Data Acquisition](#data-acquisition)
    - [Download MAF and CSV files locally:](#download-maf-and-csv-files-locally)
    - [Download reference FASTA](#download-reference-fasta)
  - [Mutational Signature Analysis](#mutational-signature-analysis)
  - [DNA Shape Prediction](#dna-shape-prediction)
  - [Data Processing and Visualization](#data-processing-and-visualization)
    - [Links to Specific Sections:](#links-to-specific-sections)

---
