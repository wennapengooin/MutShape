import pandas as pd
import numpy as np
import os
import sys

def calculate_shannon_index(row, signature_columns):
    """
    Calculates the Shannon index for a given sample.

    Args:
        row (pd.Series): Row of the DataFrame.
        signature_columns (list): List of column names for mutational signatures.

    Returns:
        float: Calculated Shannon index.
    """
    proportions = row[signature_columns] / row[signature_columns].sum()
    proportions = proportions.astype(float) # Ensure proportions are valid numbers and handle NaN values
    proportions = proportions[proportions > 0]  # Exclude zero proportions to avoid log issues
    shannon_index = -np.sum(proportions * np.log(proportions))
    return shannon_index

def add_shannon_index(input_csv):
    """
    Adds a Shannon Index column to the input CSV and saves the result.

    Args:
        input_csv (str): Path to the input CSV file.
    """
    # Load the CSV file
    df = pd.read_csv(input_csv)

    # Identify mutational signature columns (assumes the first column is sample identifier)
    signature_columns = df.columns[1:]
    print(f"Identified signature columns: {signature_columns}")

    # Calculate the Shannon Index for each row
    df['Shannon_Index'] = df.apply(calculate_shannon_index, axis=1, signature_columns=signature_columns)

    # Save the updated DataFrame to a new CSV file
    output_csv = os.path.splitext(input_csv)[0] + '_shannon.csv'
    df.to_csv(output_csv, index=False)

    print(f"Updated CSV saved to {output_csv}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <input_csv>")
        sys.exit(1)

    input_csv = sys.argv[1]
    add_shannon_index(input_csv)
