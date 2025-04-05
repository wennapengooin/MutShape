import pandas as pd
import sys
import os

def filter_snp_rows(input_file):
    """Filters rows where Variant_Type is not 'SNP'."""
    # Load the CSV file
    df = pd.read_csv(input_file)
    
    # Filter for rows where Variant_Type is 'SNP'
    df_filtered = df[df['Variant_Type'] == 'SNP']
    
    # Save the filtered DataFrame to a new file
    df_filtered.to_csv(input_file, index=False)
    print(f"Filtered file saved as: {input_file}")

# Run the filtering if the script is called directly
if __name__ == "__main__":

    input_file = sys.argv[1]
    filter_snp_rows(input_file)
