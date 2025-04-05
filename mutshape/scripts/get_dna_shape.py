import os
import subprocess
import sys

# Parse arguments
input_file = sys.argv[1]
output_dir = sys.argv[2]
feature = sys.argv[3]
layer = sys.argv[4] if len(sys.argv) != 4 else "4"  # Default to layer 4 if not provided

# Check if input file exists
if not os.path.isfile(input_file):
    print(f"Error: Input file '{input_file}' does not exist.")
    sys.exit(1)

# Create output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Get the base name of the input file without its extension
base_name = os.path.splitext(os.path.basename(input_file))[0]

# Define the output file path
output_file = os.path.join(output_dir, f"{base_name}_{feature}_layer{layer}.txt")

# Construct the Deep DNAshape command
command = [
    "deepDNAshape",
    "--file", input_file,
    "--feature", feature,
    "--layer", layer,
    "--output", output_file
]

# Run the Deep DNAshape command
try:
    subprocess.run(command, check=True)
    print(f"Output saved to {output_file}")
except subprocess.CalledProcessError as e:
    print(f"Error running Deep DNAshape command: {e}")
    sys.exit(1)

