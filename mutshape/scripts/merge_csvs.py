import os
import pandas as pd
import sys

def merge_csv_files(input_dir, output_dir, output_filename):
    """Merge all CSV files in a directory into one CSV file."""
    # Get list of all CSV files in the input directory
    csv_files = [f for f in os.listdir(input_dir) if f.endswith('.csv')]

    if not csv_files:
        print("No CSV files found in the input directory.")
        sys.exit(1)

    # Read and concatenate all CSV files
    combined_df = pd.concat(
        [pd.read_csv(os.path.join(input_dir, csv_file)) for csv_file in csv_files],
        ignore_index=True
    )

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Save the combined DataFrame to the specified output directory
    output_path = os.path.join(output_dir, output_filename)
    combined_df.to_csv(output_path, index=False)
    print(f"Merged file saved at: {output_path}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python merge_csvs.py <input_directory> <output_directory> <output_filename>")
        sys.exit(1)

    input_directory = sys.argv[1]
    output_directory = sys.argv[2]
    output_file = sys.argv[3]

    merge_csv_files(input_directory, output_directory, output_file)

