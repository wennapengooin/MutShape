import os
import sys
import pandas as pd
import numpy as np
from scipy.spatial.distance import euclidean


def calculate_euclidean_distance(mut_file, ref_file):
    """
    Calculate the Euclidean distance for each sequence (line) between two text files.
    """
    distances = []
    with open(mut_file, 'r') as mut_f, open(ref_file, 'r') as ref_f:
        mut_lines = mut_f.readlines()
        ref_lines = ref_f.readlines()

        if len(mut_lines) != len(ref_lines):
            raise ValueError("The mutated and reference files must have the same number of sequences.")

        for mut_line, ref_line in zip(mut_lines, ref_lines):
            mut_values = np.array(list(map(float, mut_line.strip().split())))
            ref_values = np.array(list(map(float, ref_line.strip().split())))
            distances.append(euclidean(mut_values, ref_values))

    return distances


def append_euclidean_to_csv(csv_file, distances, feature_name):
    """
    Append Euclidean distances to the CSV file.
    """
    df = pd.read_csv(csv_file)
    if len(df) < len(distances):
        raise ValueError("The number of rows in the CSV file is less than the number of distances.")
    df.loc[:len(distances) - 1, feature_name] = distances
    df.to_csv(csv_file, index=False)
    print(f"Appended {feature_name} distances to {csv_file}")


def calculate_sign(mut_file, ref_file):
    """
    Calculate the sign (POS, NEG, ZERO) of the sum of differences for each sequence.
    """
    signs = []
    with open(mut_file, 'r') as mut_f, open(ref_file, 'r') as ref_f:
        mut_lines = [list(map(float, line.split())) for line in mut_f]
        ref_lines = [list(map(float, line.split())) for line in ref_f]

        if len(mut_lines) != len(ref_lines):
            raise ValueError("The number of sequences in the mutation and reference files do not match.")

        for mut_seq, ref_seq in zip(mut_lines, ref_lines):
            if len(mut_seq) != len(ref_seq):
                raise ValueError("Mismatch in sequence lengths between mutation and reference files.")
            diff_sum = sum(mut - ref for mut, ref in zip(mut_seq, ref_seq))
            if diff_sum > 0:
                signs.append("POS")
            elif diff_sum < 0:
                signs.append("NEG")
            else:
                signs.append("ZERO")

    return signs


def append_sign_to_csv(csv_file, signs, feature_name):
    """
    Append signs (POS, NEG, ZERO) to the CSV file.
    """
    df = pd.read_csv(csv_file)
    column_name = f"{feature_name}_Sign"
    if column_name in df.columns:
        raise ValueError(f"The column '{column_name}' already exists in the CSV file.")
    df[column_name] = signs
    df.to_csv(csv_file, index=False)
    print(f"Appended {column_name} to {csv_file}")


def add_signed_euclidean_distance(csv_file, feature_name):
    """
    Add a signed Euclidean distance column to the CSV file.
    """
    df = pd.read_csv(csv_file)
    if feature_name not in df.columns or f"{feature_name}_Sign" not in df.columns:
        raise ValueError(f"The required columns '{feature_name}' or '{feature_name}_Sign' are missing in the input file.")

    def calculate_signed_distance(row):
        if row[f"{feature_name}_Sign"] == "POS":
            return row[feature_name]
        elif row[f"{feature_name}_Sign"] == "NEG":
            return -row[feature_name]
        elif row[f"{feature_name}_Sign"] == "ZERO":
            return 0
        else:
            raise ValueError(f"Invalid sign value '{row[f'{feature_name}_Sign']}' found.")

    df[f"{feature_name}_Signed"] = df.apply(calculate_signed_distance, axis=1)
    df.to_csv(csv_file, index=False)
    print(f"Added signed Euclidean distances to {csv_file}")


def append_dna_features(csv_file, wt_file, mut_file):
    """
    Append DNA shape values (WT and MUT) to the CSV file.
    """
    feature_name = os.path.basename(wt_file).split('_')[1].split('.')[0]
    csv_data = pd.read_csv(csv_file)

    with open(wt_file, 'r') as f:
        wt_data = [line.strip() for line in f.readlines()]

    with open(mut_file, 'r') as f:
        mut_data = [line.strip() for line in f.readlines()]

    if len(csv_data) != len(wt_data) or len(csv_data) != len(mut_data):
        raise ValueError("Mismatch in the number of rows between CSV and text files.")

    csv_data[f"{feature_name}_wt"] = wt_data
    csv_data[f"{feature_name}_mut"] = mut_data
    csv_data.to_csv(csv_file, index=False)
    print(f"Appended DNA shape values to {csv_file}")


def process_all(csv_file, mut_file, ref_file):
    """
    Process all features: calculate Euclidean distances, signs, signed distances, and DNA shape values.
    """
    feature_name = os.path.basename(mut_file).split('_')[1].split('.')[0]

    # Step 1: Calculate Euclidean distances and append to CSV
    distances = calculate_euclidean_distance(mut_file, ref_file)
    append_euclidean_to_csv(csv_file, distances, feature_name)

    # Step 2: Calculate signs and append to CSV
    signs = calculate_sign(mut_file, ref_file)
    append_sign_to_csv(csv_file, signs, feature_name)

    # Step 3: Add signed Euclidean distances to CSV
    add_signed_euclidean_distance(csv_file, feature_name)

    # Step 4: Append DNA shape values to CSV
    append_dna_features(csv_file, ref_file, mut_file)


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python process_all_features.py <csv_file> <mut_file> <ref_file>")
        sys.exit(1)

    csv_file = sys.argv[1]
    mut_file = sys.argv[2]
    ref_file = sys.argv[3]

    process_all(csv_file, mut_file, ref_file)