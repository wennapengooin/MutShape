import os
import pandas as pd
import sys

def extract_sample_name(filepath):
    """Extract the sample name from the file path."""
    return os.path.basename(filepath).split("_")[-1].replace(".txt", "")

def format_chromosome(chrom):
    """Format chromosome to match CSV file format."""
    if chrom.isnumeric():
        return f"chr{chrom}"
    return f"chr{chrom.upper()}"

def find_max_signature(row):
    # Extract SBS columns and convert to numeric
    signature_cols = [col for col in row.index if col.startswith("SBS")]
    signature_values = pd.to_numeric(row[signature_cols], errors='coerce')
    
    # Check if all values are NaN
    if signature_values.isna().all():
        return "No Signature Found"

    # Return the column name with the max value
    return signature_values.idxmax()

def process_sample(txt_file, csv_dir):
    """Process a single sample file and update the corresponding CSV."""
    sample_name = extract_sample_name(txt_file)
    csv_file = os.path.join(csv_dir, f"{sample_name}.csv")

    # Check if corresponding CSV exists
    if not os.path.isfile(csv_file):
        print(f"Sample CSV not found: {sample_name}")
        return

    # Load files
    txt_df = pd.read_csv(txt_file, sep="\t")
    csv_df = pd.read_csv(csv_file)

    # Initialize Signature column if not exists
    if "Signature" not in csv_df.columns:
        csv_df["Signature"] = None

    unmatched_count = 0

    # Match rows and assign signatures
    for _, txt_row in txt_df.iterrows():
        formatted_chrom = format_chromosome(str(txt_row["Chr"]))

        # Find corresponding mutation in the CSV
        match = csv_df[
            (csv_df["Chromosome"] == formatted_chrom) &
            (csv_df["Start_Position"] == txt_row["Pos"]) &
            (csv_df["End_Position"] == txt_row["Pos"])
        ]

        if match.empty:
            unmatched_count += 1
        else:
            max_signature = find_max_signature(txt_row)
            csv_df.loc[
                (csv_df["Chromosome"] == formatted_chrom) &
                (csv_df["Start_Position"] == txt_row["Pos"]) &
                (csv_df["End_Position"] == txt_row["Pos"]),
                "Signature"
            ] = max_signature

    # Save the updated CSV
    csv_df.to_csv(csv_file, index=False)

    print(f"Processed {sample_name}: {unmatched_count} unmatched mutations")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python append_signatures.py <txt_file> <csv_directory>")
        sys.exit(1)

    txt_file = sys.argv[1]
    csv_dir = sys.argv[2]

    if not os.path.isfile(txt_file):
        print(f"Error: TXT file not found: {txt_file}")
        sys.exit(1)

    if not os.path.isdir(csv_dir):
        print(f"Error: CSV directory not found: {csv_dir}")
        sys.exit(1)

    process_sample(txt_file, csv_dir)

