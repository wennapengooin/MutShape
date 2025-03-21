# MutShape: A Mutational Signature and DNA Shape Analysis Pipeline
==============================================

This README outlines the complete pipeline for analyzing mutational signatures and DNA shape features in cancer samples. The pipeline consists of two main components:

1. **Mutational Signature Analysis** using SigProfilerAssignment
2. **DNA Shape Prediction** using deepDNAshape

## Table of Contents
-----------------

1. [Environment Setup](#environment-setup)
2. [Data Acquisition](#data-acquisition)
3. [Mutational Signature Analysis](#mutational-signature-analysis)
4. [DNA Shape Prediction](#dna-shape-prediction)
5. [Data Processing and Visualization](#data-processing-and-visualization)

## Environment Setup
-------------------

### For SigProfilerAssignment:

```bash
module load StdEnv/2023 python scipy-stack
virtualenv --no-download ENV2
source ENV2/bin/activate
pip install --no-index --upgrade pip
pip install SigProfilerAssignment
```

### For deepDNAshape:

```bash
module load StdEnv/2023 python/3.10.13
virtualenv --no-download ENV
source ENV/bin/activate
pip install --no-index --upgrade pip
PYTHONPATH="" pip install numpy==1.23.5
pip install tensorflow==2.15.1
pip install pyfaidx
git clone https://github.com/JinsenLi/deepDNAshape
cd deepDNAshape
pip install .
```

[Detailed environment setup instructions](#environment-setup)

## Data Acquisition
------------------

### Download MAF files:

Use the provided R script to download MAF files from TCGA:

```r
library(TCGAbiolinks)
# ... (R code for downloading MAF files)
```

[Full data acquisition instructions](#data-acquisition)

## Mutational Signature Analysis
------------------------------

1. **Install Reference Genome**:
   ```python
   from SigProfilerMatrixGenerator import install as genInstall
   genInstall.install('GRCh38')
   ```

2. **Prepare MAF Files**:
   ```bash
   gzip -dr /home/wendyy/scratch/maf/{cancer}
   ```

3. **Run SigProfilerAssignment**:
   ```bash
   sbatch master_get_sig.sh
   ```

[Detailed SigProfilerAssignment instructions](#mutational-signature-analysis)

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

[Full deepDNAshape pipeline instructions](#dna-shape-prediction)

## Data Processing and Visualization
-----------------------------------

**Extract Signatures and MGW Data**:
```bash
sbatch ex_extract_sig_mgw.sh
```

[Data processing and visualization details](#data-processing-and-visualization)

For more detailed instructions on specific parts of the pipeline, please refer to the linked sections above.

### Links to Specific Sections:

- [Environment Setup](#environment-setup)
- [Data Acquisition](#data-acquisition)
- [Mutational Signature Analysis](#mutational-signature-analysis)
- [DNA Shape Prediction](#dna-shape-prediction)
- [Data Processing and Visualization](#data-processing-and-visualization)

---
