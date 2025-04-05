import os
import sys
from SigProfilerAssignment import Analyzer as Analyze

def validate_directory(directory, create_if_missing=False):
    """
    Validates if a directory exists. Optionally creates it if missing.

    Args:
        directory (str): Path to the directory.
        create_if_missing (bool): Whether to create the directory if it doesn't exist.

    Returns:
        bool: True if the directory exists or was created successfully, False otherwise.
    """
    if not os.path.isdir(directory):
        if create_if_missing:
            os.makedirs(directory)
            print(f"Created directory: {directory}")
            return True
        else:
            print(f"Error: Directory {directory} does not exist.")
            return False
    return True

def perform_signature_analysis(maf_directory, output_directory):
    """
    Performs mutational signature analysis using SigProfilerAssignment.

    Args:
        maf_directory (str): Path to the directory containing MAF files.
        output_directory (str): Path to the directory where results will be saved.
    """
    print(f"Processing MAF directory: {maf_directory}")
    Analyze.cosmic_fit(
        samples=maf_directory,
        output=output_directory,
        input_type="vcf",
        context_type="96",
        genome_build="GRCh38",
        exome=True,
        export_probabilities_per_mutation=True,
        cosmic_version=3.4
    )
    print(f"Results saved to {output_directory}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python get_sigs.py <maf_directory> <output_directory>")
        sys.exit(1)

    maf_directory = sys.argv[1]
    output_directory = sys.argv[2]

    # Validate directories
    if not validate_directory(maf_directory):
        sys.exit(1)
    validate_directory(output_directory, create_if_missing=True)

    # Perform mutational signature analysis
    perform_signature_analysis(maf_directory, output_directory)