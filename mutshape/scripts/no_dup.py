import pandas as pd
import sys

def remove_duplicate_mutations(csv_file):
    # Load the CSV file
    df = pd.read_csv(csv_file)
    
    # Count initial number of rows
    initial_rows = len(df)
    
    # Drop duplicate mutations based on specified columns
    df_unique = df.drop_duplicates(subset=["Start_Position", "Chromosome", "Entrez_Gene_Id", "Reference_Allele", "Tumor_Seq_Allele2"], keep='first')
    
    # Count remaining rows
    final_rows = len(df_unique)
    
    # Calculate the number of removed rows
    removed_rows = initial_rows - final_rows
    
    # Save the cleaned data back to the same file
    df_unique.to_csv(csv_file, index=False)
    
    print(f"Number of duplicate mutations removed: {removed_rows}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python no_dup.py <csv_file>")
        sys.exit(1)
    
    csv_file = sys.argv[1]
    remove_duplicate_mutations(csv_file)
