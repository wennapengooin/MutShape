import pandas as pd
import sys
import os

def write_flanking_sequences(input_file, output_dir, sequence_type):
    # Validate sequence type
    if sequence_type.lower() not in ["ref", "mut"]:
        print("Error: sequence_type must be 'ref' or 'mut'")
        sys.exit(1)

    # Load the CSV file
    df = pd.read_csv(input_file)

    # Determine the column to use
    column_name = "Ref_Flanking_Sequence" if sequence_type.lower() == "ref" else "Mut_Flanking_Sequence"

    # Check if the column exists
    if column_name not in df.columns:
        print(f"Error: Column '{column_name}' not found in the CSV.")
        sys.exit(1)

    # Convert sequences to uppercase
    sequences = df[column_name].str.upper()

    # Generate output file path
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    output_file = os.path.join(output_dir, f"{base_name}.txt")

    # Write sequences to the text file
    with open(output_file, "w") as f:
        for seq in sequences:
            f.write(f"{seq}\n")

    print(f"Flanking sequences written to '{output_file}'.")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python write_flanking_sequences.py <input_csv_file> <output_directory> <sequence_type ('ref' or 'mut')>")
        sys.exit(1)

    input_csv = sys.argv[1]
    output_directory = sys.argv[2]
    sequence_type_arg = sys.argv[3]

    # Validate input file
    if not os.path.isfile(input_csv):
        print(f"Error: File '{input_csv}' not found.")
        sys.exit(1)

    # Validate output directory
    if not os.path.isdir(output_directory):
        print(f"Error: Directory '{output_directory}' not found.")
        sys.exit(1)

    # Process the CSV file
    write_flanking_sequences(input_csv, output_directory, sequence_type_arg)

