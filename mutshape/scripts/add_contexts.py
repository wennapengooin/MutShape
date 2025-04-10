import os
import sys
import pandas as pd
from pyfaidx import Fasta
from sys import argv

# Define reverse complement map for bases
complement_map = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}

def load_data(file_path):
    """Load a CSV file into a DataFrame."""
    return pd.read_csv(file_path)

def save_data(df, file_path):
    """Save DataFrame to CSV."""
    df.to_csv(file_path, index=False)
    print(f"Data saved to {file_path}")

def calculate_flanking_positions(df, flank_len):
    """
    Calculate downstream and upstream positions for each mutation
    and add them as new columns to the DataFrame.
    """
    df['Downstream_Position'] = df['Start_Position'] + flank_len
    df['Upstream_Position'] = df['Start_Position'] - flank_len
    return df

def load_reference_genome(fasta_file):
    """Loads the reference genome from a FASTA file."""
    return Fasta(fasta_file)

def extract_flanking_sequence(row, reference, flank_size=10):
    """
    Extracts a flanking sequence of specified size around a mutation.
    The total sequence length will be (2 * flank_size + 1).
    """
    chrom = row['Chromosome']
    start = row['Upstream_Position'] - 1  # Convert to 0-based index
    end = row['Downstream_Position']

    try:
        # Extract sequence from reference genome
        return reference[chrom][start:end].seq
    except KeyError:
        return None

def mutate_flanking_sequence(ref_sequence, mutation_base, flank_size=10):
    """
    Returns a mutated flanking sequence by replacing the middle base with a specified mutation base.
    """
    if ref_sequence is None or len(ref_sequence) != (2 * flank_size + 1):
        return None
    
    # Replace the middle base in the sequence
    mutated_sequence = ref_sequence[:flank_size] + mutation_base + ref_sequence[flank_size + 1:]
    return mutated_sequence

def add_flanking_sequences(df, reference, flank_size=10):
    """
    Adds both `Ref_Flanking_Sequence` and `Mut_Flanking_Sequence` columns to the DataFrame.
    """
    df['Ref_Flanking_Sequence'] = df.apply(
        lambda row: extract_flanking_sequence(row, reference, flank_size), axis=1
    )
    df['Mut_Flanking_Sequence'] = df.apply(
        lambda row: mutate_flanking_sequence(row['Ref_Flanking_Sequence'], row['Tumor_Seq_Allele2'], flank_size), axis=1
    )

def get_context(chromosome, position, reverse_complement, reference):
    """Fetches the trinucleotide context for a given mutation."""
    # Convert position to zero-based for pyfaidx
    start = position - 1
    # Fetch surrounding bases from the FASTA
    context = reference[chromosome][start - 1:start + 2]
    if reverse_complement:
        context = context.reverse.complement

    context = context.seq

    upstream = context[0]
    downstream = context[2]

    return upstream, downstream

def get_trinucleotide_context(row, reference):
    """Creates trinucleotide context and reverse complement if necessary."""
    # Fetch upstream and downstream bases
    reverse_complement = False

    chromosome = row['Chromosome']
    position = int(row['Start_Position'])
    upstream, downstream = get_context(chromosome, position, reverse_complement, reference)

    # Construct the context
    ref_allele = row['Reference_Allele']
    tumor_allele = row['Tumor_Seq_Allele2']
    
    # Reverse complement if mutation originates from a purine
    if ref_allele in ['A', 'G']:
        # Reverse complement context
        reverse_complement = True
        upstream, downstream = get_context(chromosome, position, reverse_complement, reference)

        ref_allele = complement_map[ref_allele]
        tumor_allele = complement_map[tumor_allele]

    context = f"{upstream}[{ref_allele}>{tumor_allele}]{downstream}"
    
    return context, reverse_complement

def add_trinucleotide_context(df, reference):
    """
    Adds `Trinucleotide_Context` and `Reverse_Complement` columns to the DataFrame.
    """
    df[['Trinucleotide_Context', 'Reverse_Complement']] = df.apply(
        lambda row: pd.Series(get_trinucleotide_context(row, reference)), axis=1
    )

def process_mutations(input_csv, ref_fasta, flank_size=10):
    """
    Main function to process mutations: add flanking positions, sequences, and trinucleotide contexts.
    """
    # Load reference genome and input CSV data
    reference = load_reference_genome(ref_fasta)
    df = load_data(input_csv)

    # Add flanking positions
    df = calculate_flanking_positions(df, flank_size)

    # Add flanking sequences
    add_flanking_sequences(df, reference, flank_size)

    # Add trinucleotide context
    add_trinucleotide_context(df, reference)

    # Save the modified data
    save_data(df, input_csv)

    # Display the first few rows to verify
    print(df.head())

# Execute the script with command-line arguments
if __name__ == "__main__":
    if len(argv) != 3:
        print("Usage: python process_mutations.py <input_csv> <ref_fasta>")
        sys.exit(1)

    input_csv = argv[1]
    ref_fasta = argv[2]
    process_mutations(input_csv, ref_fasta)